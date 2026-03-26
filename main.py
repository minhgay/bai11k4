import streamlit as st
import google.generativeai as genai

# Cấu hình API
genai.configure(api_key=st.secrets['GOOGLE_API_KEY'])

# Lấy model text
model = genai.GenerativeModel('gemini-2.5-flash')

st.title('Choose the drink')

with st.form('Order'):
    drink_options = ("Traditional", "Matcha", "Juice")
    opt_d = st.selectbox('Choose the drink', drink_options)

    prices = {'traditional': 5, 'matcha': 7, 'juice': 8}

    opt_s = st.selectbox('Choose sugar', ('brown', 'white', 'N/A'))
    opt_t = st.selectbox('Choose jelly', ('rau câu', 'nha đam', 'N/A'))

    slg = st.slider('Số lượng', 1, 10)

    # Tính tổng
    total = prices[opt_d.lower()] * slg

    bill = {
        'Loại đồ uống': opt_d,
        'Loại đường': opt_s,
        'Loại thạch': opt_t,
        'Số lượng': slg,
        'Tổng tiền': f'{total} EUR'
    }

    sub = st.form_submit_button('Submit')

if sub:
    st.divider()
    c1, c2 = st.columns(2)

    with c1:
        st.write("Chi tiết order:")
        for x, y in bill.items():
            st.write(f"{x}: {y}")

    with c2:
        prompt = f"""
        Đóng vai trò là một nhà pha chế chuyên nghiệp, nhận xét khoảng 50-100 từ về gu của khách.
        Khách chọn: đồ uống {opt_d}, loại đường {opt_s}, loại thạch {opt_t}.
        Dùng ngôn ngữ thân thiện gửi khách hàng.
        """
        try:
            r = model.generate_content(prompt)
            st.info(r.text)
        except Exception as e:
            st.error('AI-errored: ' + str(e))

print_bill = st.checkbox('Print bill')
if print_bill and sub:
        ans = ''
        for x, y in bill.items():
            ans += f"{x}: {y}\n"
        st.download_button('In hóa đơn', data=ans, file_name="HOADON.txt")
