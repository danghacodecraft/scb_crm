from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from app.api.base.repository import ReposReturn
from app.third_parties.oracle.models.cif.form.model import (
    Booking, BookingCustomer, TransactionDaily
)
from app.third_parties.oracle.models.master_data.others import (
    Lane, Phase, Stage, StageLane, StagePhase, StageRole, StageStatus,
    TransactionStage, TransactionStageStatus
)
from app.utils.error_messages import (
    ERROR_BEGIN_STAGE_NOT_EXIST, ERROR_NEXT_RECEIVER_NOT_EXIST,
    ERROR_STAGE_NOT_EXIST
)


async def repos_get_current_stage(
        cif_id: str,
        session: Session
) -> ReposReturn:
    """
    Input:
    Output: BookingCustomer, Booking, TransactionDaily, TransactionStage
    """
    current_stage = session.execute(
        select(
            BookingCustomer,
            Booking,
            TransactionDaily,
            TransactionStage,
            TransactionStageStatus
        )
        .join(Booking, BookingCustomer.booking_id == Booking.id)
        .join(TransactionDaily, Booking.transaction_id == TransactionDaily.transaction_id)
        .join(TransactionStage, TransactionDaily.transaction_stage_id == TransactionStage.id)
        .join(TransactionStageStatus, TransactionStage.status_id == TransactionStageStatus.id)
        .filter(BookingCustomer.customer_id == cif_id)
    ).first()
    print(current_stage)

    if not current_stage:
        return ReposReturn(is_error=True, msg=ERROR_STAGE_NOT_EXIST, loc=f"cif_id {cif_id}")

    return ReposReturn(data=current_stage)


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
    next_stage_info = session.execute(
        select(
            StageStatus,
            Stage,
            # StageLane,
            # StagePhase
        )
        .join(StageStatus, Stage.status_id == StageStatus.id)
        # .join(StageLane, Stage.id == StageLane.stage_id)
        # .join(StagePhase, Stage.id == StagePhase.stage_id)
        .filter(and_(
            Stage.parent_id == current_stage_code,
            Stage.business_type_id == business_type_id
        ))
    ).first()

    if not next_stage_info:
        return ReposReturn(
            is_error=True,
            msg=ERROR_BEGIN_STAGE_NOT_EXIST,
            detail=f"business_type_id: {business_type_id}, current_stage: {current_stage_code}"
        )

    return ReposReturn(data=next_stage_info)


async def repos_get_stage_information(
        business_type_id: str,
        stage_id: str,
        session: Session
):
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
            Stage.parent_id == stage_id,
            Stage.business_type_id == business_type_id
        ))
    ).first()

    return ReposReturn(data=stage_info)


async def repos_get_next_receiver(
        business_type_id: str,
        stage_id: str,
        session: Session
):
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
        return ReposReturn(
            is_error=True,
            msg=ERROR_NEXT_RECEIVER_NOT_EXIST,
            detail=f"business_type_id: {business_type_id}, stage_id: {stage_id}"
        )

    return ReposReturn(data=next_receiver)

# async def repos_get_current_stage(
#         business_type_id: str,
#         stage_id: str,
#         session: Session
# ):
#     current_stage = session.execute(
#         select(
#             TransactionStage
#         ).filter(and_(
#             TransactionStage.business_type_id == business_type_id,
#
#         ))
#     ).scalar().first()
#
#     if not current_stage:
#         return ReposReturn(
#             is_error=True,
#             msg=ERROR_CURRENT_STAGE_NOT_EXIST,
#             detail=f"business_type_id: {business_type_id}, stage_id: {stage_id}"
#         )
#
#     return ReposReturn(data=current_stage)


# async def repos_get_stages(
#
#     session: Session
# ):
#     stages = session.execute(
#         select(
#             Stage
#         )
#         .filter(
#             Stage.business_type_id == business_type_id
#         )
#     ).all()
#
#     if not stages:
#         return ReposReturn(
#             is_error=True,
#             msg=ERROR_STAGE_NOT_EXIST,
#             detail=f"stage_id: {business_type_id}"
#         )
#
#     return ReposReturn(data=stages)


# async def repos_get_stage_by_business_type(
#         business_type_id: str,
#         stage_id: str,
#         session: Session
# ):
#     stage_data = session.execute(
#         select(
#             StageStatus,
#             Stage,
#             StageLane,
#             Lane,
#             StageRole,
#             StagePhase,
#             Phase
#         )
#         .join(StageStatus, Stage.status_id == StageStatus.id)
#         .join(StageLane, Stage.id == StageLane.stage_id)
#         .join(Lane, StageLane.lane_id == Lane.id)
#         .join(StageRole, Stage.id == StageRole.stage_id)
#         .join(StagePhase, Stage.id == StagePhase.stage_id)
#         .join(Phase, StagePhase.phase_id == Phase.id)
#         .filter(and_(
#             Stage.business_type_id == business_type_id,
#             Stage.id == stage_id
#         ))
#     ).first()
#
#     if not stage_data:
#         return ReposReturn(
#             is_error=True,
#             msg=ERROR_STAGE_NOT_EXIST,
#             loc=f"business_type_id: {business_type_id}, stage_id: {stage_id}"
#         )
#
#     return ReposReturn(data=stage_data)
