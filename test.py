import streamlit as st
from google import genai

# --- 1. ANNELERE ÖZEL, BÜYÜK VE RENKLİ TASARIM ---
st.set_page_config(page_title="Hangi Yeşilçam Sultanısın?", page_icon="🎬", layout="centered")

st.markdown("""
<style>
/* Arka planı hafif tatlı bir renk yapalım */
.stApp {
    background-color: #FFF0F5;
}
/* Yazıları ve butonları kocaman yapalım ki gözlüksüz okunsun */
html, body, [class*="css"]  {
    font-size: 22px !important; 
    font-family: 'Georgia', serif;
}
h1 {
    color: #C71585 !important;
    text-align: center;
    font-size: 40px !important;
}
.stButton>button {
    width: 100%; 
    border-radius: 15px; 
    font-size: 26px !important;
    font-weight: bold; 
    background-color: #C71585; 
    color: white;
    padding: 15px;
}
.stRadio label {
    font-size: 20px !important;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

st.title("🎬 Hangi Yeşilçam Sultanısın?")
st.markdown("### Sadece 3 soruda ruhundaki Yeşilçam efsanesini buluyoruz! 💖")
st.markdown("---")

# --- API ANAHTARI ---
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

# --- 2. ÇOK BASİT VE EĞLENCELİ SORULAR ---
soru_1 = st.radio(
    "1. Pazar sabahı uyandığında evdeki halin nasıldır? ☀️",
    [
        "Erkenden kalkar, herkese mükellef bir sofra hazırlarım. (Anaç)",
        "Kahvemi yapar, sessizliğin ve keyfin tadını çıkarırım. (Zarif)",
        "Evi toparlar, hemen işlere girişirim. Çok hamaratım! (Pratik)",
        "Süslenir püslenir, kendime bakarım. Pazar benim günümdür. (Havalı)"
    ], index=None
)

soru_2 = st.radio(
    "2. Arkadaş ortamında (veya altın gününde) sen kimsin? ☕",
    [
        "Herkesin derdini dinleyen, akıl veren o tatlı ablayım.",
        "Ortamın en şık giyineni ve en asil duranıyım.",
        "Haksızlığa gelemeyen, dobralığıyla bilinen lafını esirgemeyen kişiyim.",
        "Hep gülen, herkesi güldüren, ortamın neşe kaynağıyım."
    ], index=None
)

soru_3 = st.radio(
    "3. Hayatta en çok neye önem verirsin? 🌸",
    [
        "Ailem, yuvam ve sevdiklerim her şeyden önce gelir.",
        "Gururum, duruşum ve asaletime çok dikkat ederim.",
        "Adalet, dürüstlük ve haksızlığa boyun eğmemek.",
        "Sevgi, neşe ve hayatın tadını çıkarmak."
    ], index=None
)

st.markdown("---")

# --- 3. SONUÇ BUTONU VE YAPAY ZEKA ---
if st.button("✨ Sonucumu Göster ✨"):
    if not soru_1 or not soru_2 or not soru_3:
        st.warning("Aman canım, sonuç için lütfen tüm soruları işaretle! 🌸")
    else:
        with st.spinner("Yıldızlar inceleniyor, Yeşilçam arşivi taranıyor... 🎞️"):
            try:
                client = genai.Client(api_key=GEMINI_API_KEY)
                
                prompt = f"""
                GÖREV: Kullanıcı bir Yeşilçam kişilik testi çözdü. Verdiği cevaplar şunlar:
                1. Soru: {soru_1}
                2. Soru: {soru_2}
                3. Soru: {soru_3}
                
                Bu cevaplara bakarak onun hangi Yeşilçam kadın oyuncusuna (Türkan Şoray, Fatma Girik, Filiz Akın veya Hülya Koçyiğit) benzediğini bul.
                
                KİMLİĞİN VE TONUN: Çok tatlı dilli, övücü, karşısındaki kadına "sultanım", "harika bir kadınsın" gibi hitap eden, nostaljik bir televizyon sunucusu gibi konuş.
                
                FORMAT (Bunu doğrudan Facebook'ta paylaşacakları için ona göre yaz):
                - En üste kocaman emojilerle hangi sultan çıktığını yaz (Örn: 🌹 SEN TAM BİR TÜRKAN ŞORAY'SIN! 🌹)
                - Altına 3-4 cümleyle neden o sultan olduğunu, verdiği cevaplardan yola çıkarak çok güzel sözlerle (asil, gururlu, anaç, fedakar vs.) anlat.
                - En sona da "Sen hangi sultansın? Testi çözmek için linke tıkla!" gibi arkadaşlarını davet eden bir cümle ekle. (Link koyma, sadece cümleyi yaz).
                """
                
                res = client.models.generate_content(model='gemini-2.5-flash', contents=[prompt])
                
                st.success("İşte Ruhundaki Yeşilçam Sultanı! 🎉")
                st.info(res.text.strip())
                st.markdown("**👇 Bu harika sonucu kopyalayıp hemen Facebook'ta arkadaşlarınla paylaşabilirsin!**")
                
            except Exception as e:
                st.error(f"Sistemde ufak bir takılma oldu, lütfen tekrar bas! 🌸")
