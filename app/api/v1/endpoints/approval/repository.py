from sqlalchemy import and_, desc, select
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn
from app.third_parties.oracle.models.cif.form.model import (
    Booking, BookingCustomer, TransactionDaily
)
from app.third_parties.oracle.models.master_data.others import (
    Lane, Phase, Stage, StageLane, StagePhase, StageRole, StageStatus,
    TransactionStage, TransactionStageStatus
)
from app.utils.constant.approval import CIF_STAGE_COMPLETED, CIF_STAGE_INIT
from app.utils.error_messages import (
    ERROR_BEGIN_STAGE_NOT_EXIST, ERROR_NEXT_RECEIVER_NOT_EXIST,
    ERROR_NEXT_STAGE_NOT_EXIST
)


async def repos_get_begin_stage(business_type_id: str, session: Session):
    begin_stage = session.execute(
        select(
            StageStatus,
            Stage
        )
        .join(StageStatus, Stage.status_id == StageStatus.id)
        .filter(and_(
            Stage.parent_id.is_(None),
            Stage.business_type_id == business_type_id
        ))
    ).first()

    if not begin_stage:
        return ReposReturn(
            is_error=True,
            msg=ERROR_BEGIN_STAGE_NOT_EXIST,
            detail=f"business_type_id: {business_type_id}"
        )

    return ReposReturn(data=begin_stage)


async def repos_get_next_stage(
        business_type_id: str,
        current_stage_code: str,
        session: Session
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
            Stage.business_type_id == business_type_id
        ))
    ).scalar()

    if not next_stage_info:
        return ReposReturn(
            is_error=True,
            msg=ERROR_NEXT_STAGE_NOT_EXIST,
            detail=f"business_type_id: {business_type_id}, current_stage: {current_stage_code}"
        )

    return ReposReturn(data=next_stage_info)


async def repos_get_previous_stage(
        cif_id: str,
        session: Session
):
    """
    Trả về thông tin Stage đã lưu trong DB trước đó
    Output: BookingCustomer, Booking, TransactionDaily, TransactionStage, TransactionStageStatus
    """
    previous_stage_info = session.execute(
        select(
            BookingCustomer,
            Booking,
            TransactionDaily,
            TransactionStage,
            TransactionStageStatus
        )
        .join(Booking, BookingCustomer.booking_id == Booking.id)
        .outerjoin(TransactionDaily, Booking.transaction_id == TransactionDaily.transaction_id)
        .outerjoin(TransactionStage, TransactionDaily.transaction_stage_id == TransactionStage.id)
        .outerjoin(TransactionStageStatus, TransactionStage.status_id == TransactionStageStatus.id)
        .filter(BookingCustomer.customer_id == cif_id)
        .order_by(desc(TransactionDaily.created_at))
    ).first()

    return ReposReturn(data=previous_stage_info)


async def repos_get_stage_information(
        business_type_id: str,
        stage_id: str,
        session: Session
):
    """
    Lấy thông tin Stage
    Output: StageStatus, Stage, StageLane, Lane, StagePhase, Phase, StageRole
    """
    stage_info = session.execute(
        select(
            StageStatus,
            Stage,
            StageLane,
            Lane,
            StagePhase,
            Phase,
            StageRole
        )
        .join(StageStatus, Stage.status_id == StageStatus.id)
        .join(StageLane, Stage.id == StageLane.stage_id)
        .join(Lane, StageLane.lane_id == Lane.id)
        .join(StagePhase, Stage.id == StagePhase.stage_id)
        .join(Phase, StagePhase.phase_id == Phase.id)
        .join(StageRole, Stage.id == StageRole.stage_id)
        .filter(and_(
            Stage.id == stage_id,
            Stage.business_type_id == business_type_id
        ))
    ).first()
    if not stage_info:
        return ReposReturn(is_error=True, msg="Stage is None",
                           loc=f"stage_id: {stage_id}, business_type_id: {business_type_id}")

    return ReposReturn(data=stage_info)


async def repos_get_next_receiver(
        business_type_id: str,
        stage_id: str,
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
                Stage.parent_id == CIF_STAGE_INIT
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
                Stage.parent_id == stage_id
            )
        ).first()

        if not next_receiver:
            if stage_id == CIF_STAGE_COMPLETED:
                return ReposReturn(data=None)

            return ReposReturn(
                is_error=True,
                msg=ERROR_NEXT_RECEIVER_NOT_EXIST,
                detail=f"business_type_id: {business_type_id}, stage_id: {stage_id}"
            )
        _, next_receiver = next_receiver

    return ReposReturn(data=next_receiver)