import unicodedata
import datetime
import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import qrcode

st.title('東興QRラベル生成アプリ')

def hankaku(text):
    flg = 0
    for t in text:
        if unicodedata.east_asian_width(t) in 'FWA':
            flg = 1
    return flg

def drawText(draw,text,left,top,width,height):

    out_text_size = (width + 1, height + 1)
    font_size_offset = 0

    while width < out_text_size[0] or height < out_text_size[1]:

        font = ImageFont.truetype("./font/msgothic.ttc", 100 - font_size_offset)
        out_text_size = draw.textsize(text, font=font)
        font_size_offset += 1

    font = ImageFont.truetype("./font/msgothic.ttc", 100 - font_size_offset - 15)
    draw_text_width, draw_text_height = draw.textsize(text, font=font)
    start_X_point = (left + width / 2) - draw_text_width / 2
    start_Y_point = (top + height / 2) - draw_text_height / 2
    draw.text((start_X_point, start_Y_point), text, fill=(0, 0, 0), font=font)

def main():

    name = st.text_input("品名", placeholder="2XC", value="2XC")
    if hankaku(name): st.error('品名は半角で入力してください')

    weight = st.number_input("正味質量(kg)",value=1.00)
    
    col1, col2 = st.columns(2)
    with col1:
        size1 = st.number_input("サイズ(縦幅)",step=0.1,value=1.0)
    with col2:
        size2 = st.number_input("サイズ(横幅)",step=0.1,value=1.0)
    
    flg_lot = False
    
    if flg_lot:
        lot_num = st.text_input("ロット番号", placeholder='T-442251-1-3')
        if hankaku(lot_num): st.error('ロット番号は半角で入力してください')
    else:
        st.selectbox('ロット番号',('T-442251-1-3','T-642584-2-3'))

    flg_lot = st.checkbox('新規ロット番号')

    col1, col2 = st.columns(2)
    with col1:
        plant = st.text_input("製造工場", placeholder="刈谷工場", value="刈谷工場")
    with col2:
        line = st.text_input("製造ライン", placeholder="製造ライン B", value="製造ライン B")

    member = st.text_input("検査員", placeholder="製造部 〇〇", value="製造部 山下")
    col1, col2 = st.columns(2)
    with col1:
        test_date = st.date_input("検査日")
    with col2:
        test_time = st.time_input("検査時間")

    q = st.number_input("入り数",step=1, value=24)


    if st.button('ラベル生成'):
        if name and weight and size1 and size2 and lot_num and plant and line and member and test_date and test_time and q:
            im = Image.new('RGB', (720, 400), (255, 255, 255))
            draw = ImageDraw.Draw(im)
            draw.rectangle((20, 20, 700, 380), outline=(0, 0, 0))
            draw.rectangle((230, 20, 700, 75), outline=(0, 0, 0))
            draw.rectangle((20, 75, 700, 160), outline=(0, 0, 0))
            draw.rectangle((230, 160, 700, 215), outline=(0, 0, 0))
            draw.rectangle((20, 215, 230, 270), outline=(0, 0, 0))
            draw.rectangle((230, 270, 535, 325), outline=(0, 0, 0))
            draw.rectangle((20, 325, 230, 380), outline=(0, 0, 0))
            draw.rectangle((535, 215, 700, 380), outline=(0, 0, 0))

            drawText(draw,'場所',20 ,20 ,210, 55)
            drawText(draw,plant,230 ,20 ,470, 55)
            drawText(draw,line,20 ,75 ,680, 85)
            drawText(draw,'検査員',20 ,160 ,210, 55)
            drawText(draw,member,230 ,160 ,470, 55)
            drawText(draw,'検査日',20 ,215 ,210, 55)
            drawText(draw,test_date.strftime('%y/%m/%d'),230 ,215 ,305, 55)
            drawText(draw,'検査時間',20 ,270 ,210, 55)
            drawText(draw,test_time.strftime('(%p)%I:%M'),230 ,270 ,305, 55)
            drawText(draw,'入り数',20 ,325 ,210, 55)
            drawText(draw,str(q),230 ,325 ,305, 55)

            qr_code = qrcode.make(lot_num.replace('-','')+'000000000T0000000010000000000000000051.00')

            qr_code = qr_code.resize((163, 163))

            im.paste(qr_code, (536, 216))

            im.save('label.png', quality=95)
            st.image('./label.png')
            with open('./label.png', "rb") as file:
                btn = st.download_button(
                    label="ダウンロード",
                    data=file,
                    file_name="label.png",
                    mime="image/png"
                    )

        else:
            st.error('未入力の箇所があります')


if __name__ == '__main__':
    main()
