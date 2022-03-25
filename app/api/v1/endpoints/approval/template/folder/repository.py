from app.api.base.repository import ReposReturn


async def repos_get_approval_template_info(
    cif_id: str
):
    forms = [
        {
            "id": 1,
            "name": "01 BM MO CIF V1",
            "templates": [
                {
                    "id": 1,
                    "name": "BM_01_Giay_dang_ky_thong_tin_kiem_Hop_dong_mo_TK_va_su_dung_DV_TV",
                    "is_related_flag": True
                },
                {
                    "id": 2,
                    "name": "BM KHONG LIEN QUAN",
                    "is_related_flag": False
                },
                {
                    "id": 3,
                    "name": "BM_01_Giay_dang_ky_thong_tin_kiem_Hop_dong_mo_TK_va_su_dung_DV_SN",
                    "is_related_flag": True
                },
                {
                    "id": 4,
                    "name": "BM KHONG LIEN QUAN",
                    "is_related_flag": False
                }
            ]
        },
        {
            "id": 2,
            "name": "02_BM VCD",
            "templates": [
                {
                    "id": 1,
                    "name": "BM 01- GIAY DE NGHI MO TAI KHOAN DTGT",
                    "is_related_flag": True
                },
                {
                    "id": 2,
                    "name": "BM 02- GIAY DE NGHI MO TAI KHOAN DTTT vao VN bang VND",
                    "is_related_flag": True
                },
                {
                    "id": 3,
                    "name": "BM KHONG LIEN QUAN",
                    "is_related_flag": False
                },
                {
                    "id": 4,
                    "name": "BM 03- GIAY DE NGHI MO TAI KHOAN DTTT vao VN bang ngoai te",
                    "is_related_flag": True
                },
                {
                    "id": 5,
                    "name": "BM KHONG LIEN QUAN",
                    "is_related_flag": False
                },
                {
                    "id": 6,
                    "name": "BM 04- GIAY DE NGHI MO TAI KHOAN DTTT ra NN",
                    "is_related_flag": True
                }
            ]
        }
    ]
    return ReposReturn(data=forms)
