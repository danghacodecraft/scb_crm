# 1. Email trong trường hợp phê duyệt trạng thái Chờ hậu kiểm / cần xác minh sang Không hợp lệ
def open_ebank_failure_response(customers):
    title = "Thông báo V/v xác minh thông tin mở Tài khoản trực tuyến tại SCB."
    list_customer = ""
    if isinstance(customers, list):
        for customer in customers:
            list_customer += f"""{customer}{',' if customer != customers[-1] else ''} """

    body = f"""
            <div style="margin-left: 3%;font-size: 20px;">
            <p class="western" style="line-height: 120%; margin-top: 0.2in; margin-bottom: 0.2in;" align="justify"><span
                    lang="pt-BR"><strong>Kính gửi Quý Khách: {list_customer if isinstance(customers, list) else customers}</p>
            <p class="western" style="line-height: 120%; margin-top: 0.2in; margin-bottom: 0.2in;" align="justify"><span
                    lang="pt-BR">SCB trân trọng cảm ơn Quý Khách đã tin tưởng lựa chọn và sử dụng dịch vụ của SCB.</span></p>
            <p class="western" style="line-height: 120%; margin-top: 0.2in; margin-bottom: 0.2in;" align="justify"><span
                    lang="pt-BR">SCB kính thông báo Tài khoản thanh toán trực tuyến của Quý Khách hàng cần được xác minh thêm thông tin.
                     Quý Khách vui lòng ra SCB gần nhất hoặc liên hệ Hotline 19006538 để được hỗ trợ.</p>
            <p class="western" style="line-height: 120%; margin-top: 0.2in; margin-bottom: 0.2in;" align="justify"><span
                    style="color: #000000;"><span lang="pt-BR">Quá thời hạn 30 ngày làm việc kể từ ngày thông báo này nếu Quý Khách chưa hoàn tất xác minh thông tin,
                     SCB sẽ đóng Tài khoản và các dịch vụ liên quan Tài khoản của Quý khách theo quy định SCB.
                    </span></span></p>
            <p class="western" style="line-height: 120%; margin-top: 0.2in; margin-bottom: 0.2in;" align="justify"><span
                    lang="pt-BR">Trân trọng cảm ơn. </span></p>
            <p class="western" style="line-height: 120%; margin-top: 0.2in; margin-bottom: 0.2in;" align="justify"><span
                    lang="pt-BR"><strong>Để biết thêm thông tin, vui lòng liên hệ:</strong></span></p>
            <p class="western" style="line-height: 120%; margin-top: 0.2in; margin-bottom: 0.2in;" align="justify"><span
                    lang="pt-BR">- Hotline: 19006538</span></p>
            <p class="western" style="line-height: 120%; margin-top: 0.2in; margin-bottom: 0.2in;" align="justify"><span
                    lang="pt-BR">- Email: </span><a href="mailto:chamsockhachhang@scb.com.vn"><span
                        style="color: #0000ff;"><span
                            style="text-decoration: underline;">chamsockhachhang@scb.com.vn</span></span></a></p>
            <p class="western" style="line-height: 120%; margin-top: 0.2in; margin-bottom: 0.2in;" align="justify"><span
                    style="color: #000000;">- </span>Website:&nbsp;<a href="http://www.scb.com.vn/"
                    target="_blank"><span style="color: #0000ff;"><span
                            style="text-decoration: underline;">www.scb.com.vn</span></span></a></p>
            <p style="line-height: 120%; margin-left: 0.25in; margin-top: 0.2in; margin-bottom: 0.2in;" lang="pt-BR"
                align="justify">&nbsp;</p>
            </div>
        </div>
            """

    footer = """
            <div class="footer" style="margin-left: 3%;  font-size: 20px;">
            <p class="western" style="line-height: 120%; margin-top: 0.2in; margin-bottom: 0.2in;"><span
                    style="color: #0000ff;"><span style="color: #4472c4;"><span lang="pt-BR"><span
                                style="text-decoration: none;"><strong><img
                                        src="https://portal.scb.com.vn/newsign/scblogo-vi.png"
                                        alt="" name="Picture 2" width="157" height="59" align="left" border="0"
                                        hspace="12"/>NGÂN HÀNG THƯƠNG MẠI CỔ PHẦN SÀI GÒN</strong></span></span></span></span></p>
            <p class="western" style="line-height: 120%; margin-top: 0.2in; margin-bottom: 0.2in;"><span
                    style="color: #0000ff;"><span style="color: #000000;"><span lang="pt-BR"><span
                                style="text-decoration: none;"><strong>Điện
                                    thoại</strong></span></span></span></span><span style="color: #0000ff;"><span
                        style="color: #000000;"><span lang="pt-BR"><span style="text-decoration: none;">: (028)22228686
                                | Fax: (028)39255888</span></span></span></span></p>
            <div style="padding-left: 1.87in">
                <p class="western" style="line-height: 120%; margin-top: 0.2in; margin-bottom: 0.2in;"><a
                        name="_GoBack"></a> <span style="color: #0000ff;"><span style="color: #000000;"><span
                                lang="pt-BR"><span style="text-decoration: none;"><strong>Hội
                                        sở</strong></span></span></span></span><span style="color: #0000ff;"><span
                            style="color: #000000;"><span lang="pt-BR"><span style="text-decoration: none;">:
                                    19-21-23-25 Nguyễn Huệ, Phường Bến Nghé, Quận 1,
                                    TPHCM</span></span></span></span></p>
            </div>
        </div>
    """
    return {'title': title, 'body': body + footer}


# 2. Email trong trường hợp phê duyệt trạng thái Không hợp lệ sang Hợp lệ
def open_ebank_success_response(customers):
    title = "Thông báo V/v Tài khoản trực tuyến tại SCB kích hoạt thành công."
    list_customer = ""
    if isinstance(customers, list):
        for customer in customers:
            list_customer += f"""{customer}{',' if customer != customers[-1] else ''} """

    body = f"""
            <div style="margin-left: 3%;font-size: 20px;">
            <p class="western" style="line-height: 120%; margin-top: 0.2in; margin-bottom: 0.2in;" align="justify"><span
                    lang="pt-BR"><strong>Kính gửi Quý Khách: {list_customer if isinstance(customers, list) else customers}</p>
            <p class="western" style="line-height: 120%; margin-top: 0.2in; margin-bottom: 0.2in;" align="justify"><span
                    lang="pt-BR">SCB trân trọng cảm ơn Quý khách đã hoàn tất thủ tục xác minh thông tin.</span></p>
            <p class="western" style="line-height: 120%; margin-top: 0.2in; margin-bottom: 0.2in;" align="justify"><span
                    lang="pt-BR">SCB kính thông báo Tài khoản thanh toán trực tuyến của Quý Khách đã được kích hoạt thành công.
                     Quý Khách vui lòng đăng nhập SCB S-Connect để tiếp tục sử dụng dịch vụ.</p>
            <p class="western" style="line-height: 120%; margin-top: 0.2in; margin-bottom: 0.2in;" align="justify"><span
                    lang="pt-BR">Trân trọng cảm ơn. </span></p>
            <p class="western" style="line-height: 120%; margin-top: 0.2in; margin-bottom: 0.2in;" align="justify"><span
                    lang="pt-BR"><strong>Để biết thêm thông tin, vui lòng liên hệ:</strong></span></p>
            <p class="western" style="line-height: 120%; margin-top: 0.2in; margin-bottom: 0.2in;" align="justify"><span
                    lang="pt-BR">- Hotline: 19006538</span></p>
            <p class="western" style="line-height: 120%; margin-top: 0.2in; margin-bottom: 0.2in;" align="justify"><span
                    lang="pt-BR">- Email: </span><a href="mailto:chamsockhachhang@scb.com.vn"><span
                        style="color: #0000ff;"><span
                            style="text-decoration: underline;">chamsockhachhang@scb.com.vn</span></span></a></p>
            <p class="western" style="line-height: 120%; margin-top: 0.2in; margin-bottom: 0.2in;" align="justify"><span
                    style="color: #000000;">- </span>Website:&nbsp;<a href="http://www.scb.com.vn/"
                    target="_blank"><span style="color: #0000ff;"><span
                            style="text-decoration: underline;">www.scb.com.vn</span></span></a></p>
            <p style="line-height: 120%; margin-left: 0.25in; margin-top: 0.2in; margin-bottom: 0.2in;" lang="pt-BR"
                align="justify">&nbsp;</p>
            </div>
        </div>
            """

    footer = """
            <div class="footer" style="margin-left: 3%;  font-size: 20px;">
            <p class="western" style="line-height: 120%; margin-top: 0.2in; margin-bottom: 0.2in;"><span
                    style="color: #0000ff;"><span style="color: #4472c4;"><span lang="pt-BR"><span
                                style="text-decoration: none;"><strong><img
                                        src="https://portal.scb.com.vn/newsign/scblogo-vi.png"
                                        alt="" name="Picture 2" width="157" height="59" align="left" border="0"
                                        hspace="12"/>NGÂN HÀNG THƯƠNG MẠI CỔ PHẦN SÀI GÒN</strong></span></span></span></span></p>
            <p class="western" style="line-height: 120%; margin-top: 0.2in; margin-bottom: 0.2in;"><span
                    style="color: #0000ff;"><span style="color: #000000;"><span lang="pt-BR"><span
                                style="text-decoration: none;"><strong>Điện
                                    thoại</strong></span></span></span></span><span style="color: #0000ff;"><span
                        style="color: #000000;"><span lang="pt-BR"><span style="text-decoration: none;">: (028)22228686
                                | Fax: (028)39255888</span></span></span></span></p>
            <div style="padding-left: 1.87in">
                <p class="western" style="line-height: 120%; margin-top: 0.2in; margin-bottom: 0.2in;"><a
                        name="_GoBack"></a> <span style="color: #0000ff;"><span style="color: #000000;"><span
                                lang="pt-BR"><span style="text-decoration: none;"><strong>Hội
                                        sở</strong></span></span></span></span><span style="color: #0000ff;"><span
                            style="color: #000000;"><span lang="pt-BR"><span style="text-decoration: none;">:
                                    19-21-23-25 Nguyễn Huệ, Phường Bến Nghé, Quận 1,
                                    TPHCM</span></span></span></span></p>
            </div>
        </div>
    """
    return {'title': title, 'body': body + footer}
