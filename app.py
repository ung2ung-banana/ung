import streamlit as st
import pytesseract
from PIL import Image
import re
from collections import defaultdict

스마트폰 화면에 맞춘 레이아웃 설정
st.set_page_config(page_title="출역일보 자동 취합", page_icon="🏗️")

st.title("🏗️ 철근 이주호팀 데스라 취합")
st.markdown("스마트폰 갤러리에서 현장 카톡 스크린샷을 선택해 업로드하세요.")

모바일 다중 이미지 업로드 창
uploaded_files = st.file_uploader("카톡 캡처 이미지 업로드 (여러 장 가능)", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

if uploaded_files:
if st.button("출퇴근 현황 취합하기", type="primary"):
with st.spinner("이미지에서 글자를 읽는 중입니다..."):
attendance_data = defaultdict(list)
# 이름, 출근형태, 퇴근형태, 공수 추출 정규식
pattern = re.compile(r'([가-힣]{2,4})\s*.?((?:주간|철야|조출)\s출근)\s*(.?퇴근)\s([0-9]+.[0-9]+|[0-9]+)')

for file in uploaded_files:
try:
image = Image.open(file)
text = pytesseract.image_to_string(image, lang='kor')

for line in text.split('\n'):
line = line.strip()
if not line: continue
match = pattern.search(line)
if match:
name = match.group(1)
in_type = match.group(2).replace(" ", "")
out_type = match.group(3).replace(" ", "")
work_hours = float(match.group(4))
key = (in_type, out_type, work_hours)
if name not in attendance_data[key]:
attendance_data[key].append(name)
except Exception as e:
st.error(f"오류 발생: {file.name}\n{e}")

# 데스라 양식 텍스트화
result_text = ""
for (in_type, out_type, hours), names in sorted(attendance_data.items(), key=lambda x: (x[0][2], x[0][0])):
result_text += f"{in_type} {out_type} {hours} ({len(names)}명)\n"
for i in range(0, len(names), 5):
result_text += " ".join(names[i:i+5]) + "\n"
result_text += "\n"

if result_text:
st.success("취합 완료! 아래 텍스트를 길게 눌러 복사하신 후 단톡방에 붙여넣기 하세요.")
st.text_area("데스라 결과 (복사 가능)", result_text, height=350)
else:
st.warning("인식된 출퇴근 기록이 없습니다. 이미지 화질이나 잘린 부분을 확인해주세요.")