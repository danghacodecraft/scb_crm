from datetime import date
from typing import List, Optional

from pydantic import Field, validator

from app.api.base.schema import BaseGWSchema, BaseSchema


class SelectStatisticBankingByPeriodRequest(BaseSchema):
    from_date: date = Field(..., description="Từ ngày")
    to_date: date = Field(..., description="Đến ngày")


class SelectStatisticBankingByPeriodTotalEntryItemResponse(BaseGWSchema):
    criterion_id: Optional[str] = Field(..., description="")
    criterion_name: Optional[str] = Field(..., description="Tên tiêu chí")
    criterion_amt_day: Optional[str] = Field(..., description="Số lượng trung bình ngày")
    criterion_amt_week: Optional[str] = Field(..., description="Số lượng trung bình tuần")
    criterion_amt_month: Optional[str] = Field(..., description="Số lượng trung bình tháng")
    criterion_amt_year: Optional[str] = Field(..., description="Số lượng trung bình năm")
    criterion_title: Optional[str] = Field(..., description="Tiêu đề của tiêu chí")
    criterion_unit: Optional[str] = Field(..., description="Đơn vị của tiêu chí")
    criterion_amt_pre_period: Optional[str] = Field(..., description="Số lượng của kỳ trước")
    criterion_area_id: Optional[str] = Field(..., description="Mã vùng")
    criterion_area_name: Optional[str] = Field(..., description="Tên vùng")
    criterion_division_id: Optional[str] = Field(..., description="")
    criterion_divisior_bal_lcl: Optional[str] = Field(..., description="")
    criterion_divider_bal_lcl: Optional[str] = Field(..., description="")


class SelectStatisticBankingByPeriodTotalEntryListResponse(BaseGWSchema):
    total_entry_item: SelectStatisticBankingByPeriodTotalEntryItemResponse


class SelectStatisticBankingByPeriodTotalGrowthPercentItemResponse(BaseGWSchema):
    criterion_id: Optional[str] = Field(..., description="")
    criterion_name: Optional[str] = Field(..., description="Tên tiêu chí")
    criterion_amt_day: Optional[str] = Field(..., description="Số lượng trung bình ngày")
    criterion_amt_week: Optional[str] = Field(..., description="Số lượng trung bình tuần")
    criterion_amt_month: Optional[str] = Field(..., description="Số lượng trung bình tháng")
    criterion_amt_year: Optional[str] = Field(..., description="Số lượng trung bình năm")
    criterion_title: Optional[str] = Field(..., description="Tiêu đề của tiêu chí")
    criterion_unit: Optional[str] = Field(..., description="Đơn vị của tiêu chí")
    criterion_amt_pre_period: Optional[str] = Field(..., description="Số lượng của kỳ trước")
    criterion_area_id: Optional[str] = Field(..., description="Mã vùng")
    criterion_area_name: Optional[str] = Field(..., description="Tên vùng")
    criterion_division_id: Optional[str] = Field(..., description="")
    criterion_divisior_bal_lcl: Optional[str] = Field(..., description="")
    criterion_divider_bal_lcl: Optional[str] = Field(..., description="")


class SelectStatisticBankingByPeriodTotalGrowthPercentlistResponse(BaseGWSchema):
    total_growth_percent_item: SelectStatisticBankingByPeriodTotalGrowthPercentItemResponse


class SelectStatisticBankingByPeriodCifOpenItemResponse(BaseGWSchema):
    criterion_id: Optional[str] = Field(..., description="")
    criterion_name: Optional[str] = Field(..., description="Tên tiêu chí")
    criterion_amt_day: Optional[str] = Field(..., description="Số lượng trung bình ngày")
    criterion_amt_week: Optional[str] = Field(..., description="Số lượng trung bình tuần")
    criterion_amt_month: Optional[str] = Field(..., description="Số lượng trung bình tháng")
    criterion_amt_year: Optional[str] = Field(..., description="Số lượng trung bình năm")
    criterion_title: Optional[str] = Field(..., description="Tiêu đề của tiêu chí")
    criterion_unit: Optional[str] = Field(..., description="Đơn vị của tiêu chí")
    criterion_amt_pre_period: Optional[str] = Field(..., description="Số lượng của kỳ trước")
    criterion_area_id: Optional[str] = Field(..., description="Mã vùng")
    criterion_area_name: Optional[str] = Field(..., description="Tên vùng")
    criterion_division_id: Optional[str] = Field(..., description="")
    criterion_divisior_bal_lcl: Optional[str] = Field(..., description="")
    criterion_divider_bal_lcl: Optional[str] = Field(..., description="")


class SelectStatisticBankingByPeriodCifOpenlistResponse(BaseGWSchema):
    total_cif_open_item: SelectStatisticBankingByPeriodCifOpenItemResponse


class SelectStatisticBankingByPeriodTotalAccountCasaOpenItemResponse(BaseGWSchema):
    criterion_id: Optional[str] = Field(..., description="")
    criterion_name: Optional[str] = Field(..., description="Tên tiêu chí")
    criterion_amt_day: Optional[str] = Field(..., description="Số lượng trung bình ngày")
    criterion_amt_week: Optional[str] = Field(..., description="Số lượng trung bình tuần")
    criterion_amt_month: Optional[str] = Field(..., description="Số lượng trung bình tháng")
    criterion_amt_year: Optional[str] = Field(..., description="Số lượng trung bình năm")
    criterion_title: Optional[str] = Field(..., description="Tiêu đề của tiêu chí")
    criterion_unit: Optional[str] = Field(..., description="Đơn vị của tiêu chí")
    criterion_amt_pre_period: Optional[str] = Field(..., description="Số lượng của kỳ trước")
    criterion_area_id: Optional[str] = Field(..., description="Mã vùng")
    criterion_area_name: Optional[str] = Field(..., description="Tên vùng")
    criterion_division_id: Optional[str] = Field(..., description="")
    criterion_divisior_bal_lcl: Optional[str] = Field(..., description="")
    criterion_divider_bal_lcl: Optional[str] = Field(..., description="")


class SelectStatisticBankingByPeriodTotalAccountCasaOpenListResponse(BaseGWSchema):
    total_account_casa_open_item: SelectStatisticBankingByPeriodTotalAccountCasaOpenItemResponse


class SelectStatisticBankingByPeriodTotalDebitCardOpenItemResponse(BaseGWSchema):
    criterion_id: Optional[str] = Field(..., description="")
    criterion_name: Optional[str] = Field(..., description="Tên tiêu chí")
    criterion_amt_day: Optional[str] = Field(..., description="Số lượng trung bình ngày")
    criterion_amt_week: Optional[str] = Field(..., description="Số lượng trung bình tuần")
    criterion_amt_month: Optional[str] = Field(..., description="Số lượng trung bình tháng")
    criterion_amt_year: Optional[str] = Field(..., description="Số lượng trung bình năm")
    criterion_title: Optional[str] = Field(..., description="Tiêu đề của tiêu chí")
    criterion_unit: Optional[str] = Field(..., description="Đơn vị của tiêu chí")
    criterion_amt_pre_period: Optional[str] = Field(..., description="Đơn vị của tiêu chí")
    criterion_area_id: Optional[str] = Field(..., description="Mã vùng")
    criterion_area_name: Optional[str] = Field(..., description="Tên vùng")
    criterion_division_id: Optional[str] = Field(..., description="")
    criterion_divisior_bal_lcl: Optional[str] = Field(..., description="")
    criterion_divider_bal_lcl: Optional[str] = Field(..., description="")


class SelectStatisticBankingByPeriodTotalDebitCardOpenListResponse(BaseGWSchema):
    total_debit_card_open_item: SelectStatisticBankingByPeriodTotalDebitCardOpenItemResponse


class SelectStatisticBankingByPeriodTotalEbankOpenItemResponse(BaseGWSchema):
    criterion_id: Optional[str] = Field(..., description="")
    criterion_name: Optional[str] = Field(..., description="Tên tiêu chí")
    criterion_amt_day: Optional[str] = Field(..., description="Số lượng trung bình ngày")
    criterion_amt_week: Optional[str] = Field(..., description="Số lượng trung bình tuần")
    criterion_amt_month: Optional[str] = Field(..., description="Số lượng trung bình tháng")
    criterion_amt_year: Optional[str] = Field(..., description="Số lượng trung bình năm")
    criterion_title: Optional[str] = Field(..., description="Tiêu đề của tiêu chí")
    criterion_unit: Optional[str] = Field(..., description="Đơn vị của tiêu chí")
    criterion_amt_pre_period: Optional[str] = Field(..., description="Số lượng của kỳ trước")
    criterion_area_id: Optional[str] = Field(..., description="Mã vùng")
    criterion_area_name: Optional[str] = Field(..., description="Tên vùng")
    criterion_division_id: Optional[str] = Field(..., description="")
    criterion_divisior_bal_lcl: Optional[str] = Field(..., description="")
    criterion_divider_bal_lcl: Optional[str] = Field(..., description="")


class SelectStatisticBankingByPeriodTotalEbankOpenListResponse(BaseGWSchema):
    total_ebank_open_item: SelectStatisticBankingByPeriodTotalEbankOpenItemResponse


class SelectStatisticBankingByPeriodTotalCreditCardOpenItemResponse(BaseGWSchema):
    criterion_id: Optional[str] = Field(..., description="")
    criterion_name: Optional[str] = Field(..., description="Tên tiêu chí")
    criterion_amt_day: Optional[str] = Field(..., description="Số lượng trung bình ngày")
    criterion_amt_week: Optional[str] = Field(..., description="Số lượng trung bình tuần")
    criterion_amt_month: Optional[str] = Field(..., description="Số lượng trung bình tháng")
    criterion_amt_year: Optional[str] = Field(..., description="Số lượng trung bình năm")
    criterion_title: Optional[str] = Field(..., description="Tiêu đề của tiêu chí")
    criterion_unit: Optional[str] = Field(..., description="Đơn vị của tiêu chí")
    criterion_amt_pre_period: Optional[str] = Field(..., description="Số lượng của kỳ trước")
    criterion_area_id: Optional[str] = Field(..., description="Mã vùng")
    criterion_area_name: Optional[str] = Field(..., description="Tên vùng")
    criterion_division_id: Optional[str] = Field(..., description="")
    criterion_divisior_bal_lcl: Optional[str] = Field(..., description="")
    criterion_divider_bal_lcl: Optional[str] = Field(..., description="")


class SelectStatisticBankingByPeriodTotalCreditCardOpenListResponse(BaseGWSchema):
    total_credit_card_open_item: SelectStatisticBankingByPeriodTotalCreditCardOpenItemResponse


class SelectStatisticBankingByPeriodDataOutput(BaseGWSchema):
    total_entry_list: List[SelectStatisticBankingByPeriodTotalEntryListResponse]
    total_growth_percent_list: List[SelectStatisticBankingByPeriodTotalGrowthPercentlistResponse]
    total_cif_open_list: List[SelectStatisticBankingByPeriodCifOpenlistResponse]
    total_account_casa_open_list: List[SelectStatisticBankingByPeriodTotalAccountCasaOpenListResponse]
    total_debit_card_open_list: List[SelectStatisticBankingByPeriodTotalDebitCardOpenListResponse]
    total_ebank_open_list: List[SelectStatisticBankingByPeriodTotalEbankOpenListResponse]
    total_credit_card_open_list: List[SelectStatisticBankingByPeriodTotalCreditCardOpenListResponse]


class SelectSummaryCardsByDateRequest(BaseSchema):
    region_id: str = Field('ALL', description="Mã vùng")
    branch_code: str = Field('ALL', description="Mã chi nhánh")


class OpenSaleInternationalCardResponse(BaseGWSchema):
    criterion_amt_week: int = Field(..., description="Tuần")
    criterion_amt_month: int = Field(..., description="Tháng")
    accumulated: int = Field(..., description="Lũy kế")


class InternationalCardResponse(BaseGWSchema):
    open: OpenSaleInternationalCardResponse = Field(..., description='Số lượng thẻ phát hành mới')
    sales: OpenSaleInternationalCardResponse = Field(..., description='Doanh số thẻ')


class SelectSummaryCardsByDateResponse(BaseGWSchema):
    international_debit_card: InternationalCardResponse = Field(..., description="Thông tin thẻ thanh toán quốc tế")
    international_credit_card: InternationalCardResponse = Field(..., description="Thông tin thẻ tín dụng quốc tế")


class SelectDataForChardDashBoardRequest(BaseSchema):
    from_date: date = Field(..., description="Từ ngày")
    to_date: date = Field(..., description="Đến ngày")
    region_id: str = Field('ALL', description="Mã vùng")
    branch_code: str = Field('ALL', description="Mã chi nhánh")


class PercentSelectDataForChardDashBoardResponse(BaseGWSchema):
    cif_open_count: Optional[float] = Field(..., description="Mở CIF")
    tktt_open_count: Optional[float] = Field(..., description="Mở Tiết Kiệm")
    tktt_count_close_count: Optional[float] = Field(..., description="Tất toán")
    tktt_td_count: Optional[float] = Field(..., description="Thẻ")
    count_mortgage_loan_count: Optional[float] = Field(..., description="Vay Cầm Cố")
    other: Optional[float] = Field(..., description="Khác")

    @validator('*')
    def check_negative_number(cls, number):
        if number < 0:
            return 0
        return number


class TotalSelectDataForChardDashBoardResponse(PercentSelectDataForChardDashBoardResponse):
    company_customer_open_count: int = Field(..., description="Khách hàng mới - Khối DN")
    individual_customer_open_count: int = Field(..., description="Khách hàng mới - Khối PFS")
    total_trn_ref_no_count: int = Field(..., description="Tổng số bút toán")


class SelectDataForChardDashBoardResponse(BaseGWSchema):
    total: TotalSelectDataForChardDashBoardResponse = Field(..., description="")
    percent: PercentSelectDataForChardDashBoardResponse = Field(..., description="")
