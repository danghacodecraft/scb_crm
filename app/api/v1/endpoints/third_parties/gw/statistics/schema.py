from datetime import date
from typing import List, Optional

from pydantic import Field

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
    from_date: date = Field(..., description="Từ ngày")
    to_date: date = Field(..., description="Đến ngày")


class SelectSummaryCardsByDateResponse(BaseGWSchema):
    pass
