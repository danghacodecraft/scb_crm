from sqlalchemy import and_, desc, select
from sqlalchemy.orm import Session, aliased

from app.api.base.repository import ReposReturn
from app.third_parties.oracle.models.cif.form.model import (
    Booking, BookingCustomer, TransactionDaily, TransactionSender
)
from app.third_parties.oracle.models.master_data.others import (
    Lane, Phase, Stage, StageAction, StageLane, StagePhase, StageRole,
    StageStatus, TransactionStage, TransactionStageAction,
    TransactionStageStatus, BusinessType, Sla, BusinessJob, BusinessForm
)
from app.utils.constant.approval import (
    CIF_STAGE_APPROVE_KSS, CIF_STAGE_BEGIN, CIF_STAGE_INIT, INIT_STAGES
)
from app.utils.constant.business_type import BUSINESS_TYPE_INIT_CIF
from app.utils.error_messages import (
    ERROR_BEGIN_STAGE_NOT_EXIST, ERROR_NEXT_RECEIVER_NOT_EXIST,
    ERROR_NEXT_STAGE_NOT_EXIST
)


async def repos_get_begin_stage(business_type_id: str, session: Session):
    begin_stage = session.execute(
        select(
            StageStatus,
            Stage,
            StagePhase,
            Phase,
            StageLane,
            Lane,
            StageRole,
            Sla,
            BusinessJob,
            BusinessForm
        )
        .join(StageStatus, Stage.status_id == StageStatus.id)
        .join(Lane, Stage.business_type_id == Lane.business_type_id)
        .join(StageLane, Stage.id == StageLane.stage_id)
        .join(StagePhase, Stage.id == StagePhase.stage_id)
        .join(Phase, StagePhase.phase_id == Phase.id)
        .join(StageRole, Stage.id == StageRole.stage_id)
        .join(Sla, Stage.sla_id == Sla.id)
        .join(BusinessJob, and_(
            Stage.business_type_id == BusinessJob.business_type_id,
            BusinessJob.order_no == 1
        ))
        .join(BusinessForm, and_(
            Stage.business_type_id == BusinessForm.business_type_id,
            BusinessForm.order_no == 1
        ))
        .filter(and_(
            Stage.parent_id.is_(None),
            Stage.business_type_id == business_type_id
        ))
    ).first()

    if not begin_stage:
        return ReposReturn(
            is_error=True,
            msg=ERROR_BEGIN_STAGE_NOT_EXIST,
            detail=f"business_type_id: {business_type_id}",
            loc="repos_get_begin_stage"
        )

    return ReposReturn(data=begin_stage)


async def repos_get_stage_teller(business_type_id: str, session: Session):
    stage_id = f'{business_type_id}_{CIF_STAGE_INIT}' if business_type_id != BUSINESS_TYPE_INIT_CIF else CIF_STAGE_INIT
    stage_teller = session.execute(
        select(
            Stage
        )
        .filter(and_(
            Stage.id == stage_id,
            Stage.business_type_id == business_type_id
        ))
    ).scalar()

    if not stage_teller:
        return ReposReturn(
            is_error=True,
            msg=ERROR_BEGIN_STAGE_NOT_EXIST,
            detail=f"business_type_id: {business_type_id}"
        )

    return ReposReturn(data=stage_teller)


async def repos_get_next_stage(
    business_type_id: str,
    current_stage_code: str,
    session: Session,
    reject_flag: bool = False
):
    """
    Trả về thông tin Stage tiếp theo
    Output: Stage
    """
    next_stage_info = session.execute(
        select(
            Stage
        )
        .filter(and_(
            Stage.parent_id == current_stage_code,
            Stage.business_type_id == business_type_id,
            Stage.is_reject == reject_flag
        ))
    ).scalar()

    if not next_stage_info:
        return ReposReturn(
            is_error=True,
            msg=ERROR_NEXT_STAGE_NOT_EXIST,
            detail=f"business_type_id: {business_type_id}, current_stage: {current_stage_code}"
        )

    return ReposReturn(data=next_stage_info)


async def repos_open_cif_get_previous_stage(
        booking_id: str,
        session: Session
):
    """
    Trả về thông tin Stage đã lưu trong DB trước đó
    Output: Booking, TransactionDaily, TransactionStage, TransactionStageStatus, TransactionSender
    """
    previous_stage_info = session.execute(
        select(
            Booking,
            TransactionDaily,
            TransactionStage,
            TransactionStageStatus,
            TransactionSender,
            TransactionStageAction
        )
        .outerjoin(TransactionDaily, Booking.transaction_id == TransactionDaily.transaction_id)
        .join(TransactionStage, (TransactionDaily.transaction_stage_id == TransactionStage.id))
        .outerjoin(TransactionStageStatus, TransactionStage.status_id == TransactionStageStatus.id)
        .outerjoin(TransactionSender, TransactionDaily.transaction_id == TransactionSender.transaction_id)
        .outerjoin(TransactionStageAction, TransactionStage.action_id == TransactionStageAction.id)
        .filter(Booking.id == booking_id)
        .order_by(desc(TransactionDaily.created_at))
    ).first()

    return ReposReturn(data=previous_stage_info)


async def repos_get_previous_transaction_daily(
        transaction_daily_id: str,
        session: Session
):
    """
    Lấy thông tin Transaction Daily trước đó
    """
    previous_transaction_daily = aliased(TransactionDaily, name='PreviousTransactionDaily')
    previous_transaction_daily_info = session.execute(
        select(
            previous_transaction_daily,
            TransactionSender,
            TransactionStage,
            TransactionDaily,
            TransactionStageAction
        )
        .join(previous_transaction_daily, TransactionDaily.transaction_parent_id == previous_transaction_daily.transaction_id)
        .join(TransactionSender, previous_transaction_daily.transaction_id == TransactionSender.transaction_id)
        .join(TransactionStage, previous_transaction_daily.transaction_stage_id == TransactionStage.id)
        .join(TransactionStageAction, TransactionStage.action_id == TransactionStageAction.id)
        .filter(TransactionDaily.transaction_id == transaction_daily_id)
    ).first()

    return ReposReturn(data=previous_transaction_daily_info)


async def repos_get_begin_transaction_daily(
        cif_id: str,
        session: Session
):
    begin_transaction_daily = session.execute(
        select(
            TransactionDaily,
            TransactionStage,
            Booking,
            BookingCustomer,
            TransactionSender
        )
        .join(Booking, TransactionDaily.transaction_id == Booking.transaction_id)
        .join(BookingCustomer, and_(
            Booking.id == BookingCustomer.booking_id,
            BookingCustomer.customer_id == cif_id
        ))
        .join(TransactionSender, TransactionDaily.transaction_id == TransactionSender.transaction_id)
        .join(TransactionStage, TransactionDaily.transaction_stage_id == TransactionStage.id)
        .filter(TransactionDaily.transaction_parent_id.is_(None))
    ).first()

    return ReposReturn(data=begin_transaction_daily)


async def repos_get_stage_information(
        business_type_id: str,
        stage_id: str,
        session: Session,
        reject_flag: bool,
        stage_action_id: str,
        is_give_back: bool = False
):
    """
    Lấy thông tin Stage
    Output: StageStatus, Stage, StageLane, Lane, StagePhase, Phase, StageRole
    """
    if is_give_back:
        # Nếu trả lại hồ sơ set reject flag để Khởi tạo hồ sơ lấy đc data
        reject_flag = False
    if stage_id in INIT_STAGES:
        reject_flag = False

    stage_info = session.execute(
        select(
            StageStatus,
            Stage,
            StageLane,
            Lane,
            StagePhase,
            Phase,
            StageRole,
            StageAction,
            Sla
        )
        .join(StageStatus, Stage.status_id == StageStatus.id)
        .outerjoin(StageLane, Stage.id == StageLane.stage_id)
        .outerjoin(Lane, StageLane.lane_id == Lane.id)
        .outerjoin(StagePhase, Stage.id == StagePhase.stage_id)
        .outerjoin(Phase, StagePhase.phase_id == Phase.id)
        .outerjoin(StageRole, Stage.id == StageRole.stage_id)
        .join(Sla, Stage.sla_id == Sla.id)
        .outerjoin(StageAction, and_(
            Stage.id == StageAction.stage_id,
            StageAction.id == stage_action_id,
            StageAction.is_reject == reject_flag
        ))
        .filter(and_(
            Stage.id == stage_id,
            Stage.business_type_id == business_type_id,
            Stage.is_reject == reject_flag
        ))
    ).first()
    if not stage_info:
        return ReposReturn(is_error=True, msg="Stage is None",
                           loc=f"stage_id: {stage_id}, business_type_id: {business_type_id}, reject_flag: {reject_flag}")

    return ReposReturn(data=stage_info)


async def repos_get_next_receiver(
        business_type_id: str,
        current_stage_id: str,
        reject_flag: bool,
        session: Session
):
    """
    Output: StageLane
    """
    # Nếu từ chối phê duyệt -> Người nhận là GDV
    if reject_flag:
        _, next_receiver = session.execute(
            select(
                Stage,
                StageLane
            )
            .join(StageLane, Stage.id == StageLane.stage_id)
            .filter(
                Stage.parent_id == CIF_STAGE_BEGIN
            )
        ).first()
    else:
        next_receiver = session.execute(
            select(
                Stage,
                StageLane
            )
            .join(StageLane, Stage.id == StageLane.stage_id)
            .filter(
                Stage.parent_id == current_stage_id
            )
        ).first()

        if not next_receiver:
            if current_stage_id == CIF_STAGE_APPROVE_KSS:
                return ReposReturn(data=None)

            return ReposReturn(
                is_error=True,
                msg=ERROR_NEXT_RECEIVER_NOT_EXIST,
                detail=f"business_type_id: {business_type_id}, stage_id: {current_stage_id}"
            )
        _, next_receiver = next_receiver

    return ReposReturn(data=next_receiver)


async def repos_get_previous_stage(booking_id: str, session: Session):
    previous_stage_info = session.execute(
        select(
            Booking,
            TransactionDaily,
            TransactionStage
        )
        .join(TransactionDaily, Booking.transaction_id == TransactionDaily.transaction_id)
        .join(TransactionStage, TransactionDaily.transaction_stage_id == TransactionStage.id)
        .filter(Booking.id == booking_id)
    ).first()

    if not previous_stage_info:
        return ReposReturn(is_error=True, msg="Previous Transaction Daily is not exist, please create")

    return ReposReturn(data=previous_stage_info)


async def repos_get_stage_codes_in_business(business_type_code: str, session: Session):
    """
    Lấy những bước giao dịch trong 1 nghiệp vụ
    """
    stages_codes = session.execute(
        select(
            Stage.code,
            BusinessType
        )
        .join(Stage, BusinessType.id == Stage.business_type_id)
        .filter(BusinessType.id == business_type_code)
    ).scalars().all()
    return ReposReturn(data=stages_codes)
