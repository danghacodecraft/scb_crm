# #
# #
# def combine_full_address(number_and_street: str = None, ward: str = None, district: str = None, province: str = None):
#     if ward or district or province:
#         address = f"{number_and_street}, " if number_and_street else ""
#     else:
#         return number_and_street if number_and_street else "rong"
#     if district or province:
#         if ward and ward != "":
#             address = address + f"{ward}, "
#         if province:
#             if district:
#                 address = address + f"{district}, "
#             address = address + f"{province}"
#         else:
#             address += district
#     else:
#         address += ward
#
#     return address
# #
# ssss = '860/16 Huỳnh tấn phát'
# wwww = 'Phường Tân Phú'
# dddd = 'Quận 7'
# pppp = '1234'
#
#
# # ssss = '1'
# # wwww = '1'
# # dddd = '1'
# # pppp = '1'
#
# lst = [
#     (None, None, None, None),
#     (ssss, None, None, None),
#     (None, wwww, None, None),
#     (ssss, wwww, None, None),
#     (None, None, dddd, None),
#     (ssss, None, dddd, None),
#     (None, wwww, dddd, None),
#     (ssss, wwww, dddd, None),
#     (None, None, None, pppp),
#     (ssss, None, None, pppp),
#     (None, wwww, None, pppp),
#     (ssss, wwww, None, pppp),
#     (None, None, dddd, pppp),
#     (ssss, None, dddd, pppp),
#     (None, wwww, dddd, pppp),
#     (ssss, wwww, dddd, pppp),
# ]
# # lst = [
# #     (0, 0, 0, 0),
# #     (0, 0, 0, 1),
# #     (0, 0, 1, 0),
# #     (0, 0, 1, 1),
# #     (0, 1, 0, 0),
# #     (0, 1, 0, 1),
# #     (0, 1, 1, 0),
# #     (0, 1, 1, 1),
# #     (1, 0, 0, 0),
# #     (1, 0, 0, 1),
# #     (1, 0, 1, 0),
# #     (1, 0, 1, 1),
# #     (1, 1, 0, 0),
# #     (1, 1, 0, 1),
# #     (1, 1, 1, 0),
# #     (1, 1, 1, 1),
# # ]
#
# #
# #
# lst_2 = [
#     ("", "", "", ""),
#     (ssss, "", "", ""),
#     ("", wwww, "", ""),
#     (ssss, wwww, "", ""),
#     ("", "", dddd, ""),
#     (ssss, "", dddd, ""),
#     ("", wwww, dddd, ""),
#     (ssss, wwww, dddd, ""),
#     ("", "", "", pppp),
#     (ssss, "", "", pppp),
#     ("", wwww, "", pppp),
#     (ssss, wwww, "", pppp),
#     ("", "", dddd, pppp),
#     (ssss, "", dddd, pppp),
#     ("", wwww, dddd, pppp),
#     (ssss, wwww, dddd, pppp),
# ]
#
# def combine_full_address(number_and_street: str = None, ward: str = None, district: str = None, province: str = None):
#     if ward or district or province:
#         address = f"{number_and_street}, " if number_and_street else ""
#     else:
#         return number_and_street if number_and_street else ""
#     if district or province:
#         if ward:
#             address = address + f"{ward}, "
#         if province:
#             if district:
#                 address = address + f"{district}, "
#             address = address + f"{province}"
#         else:
#             address += district
#     else:
#         address += ward
#
#     return address
#
# for idx, item in enumerate(lst_2):
#     print(idx+1, " - ",combine_full_address(item[0], item[1], item[2], item[3]))
