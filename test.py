import streamlit as st
from google import genai

# --- 1. HERKES İÇİN NOSTALJİK TASARIM (Koyu Yazı Düzeltmeli) ---
st.set_page_config(page_title="Yeşilçam Efsane Testi", page_icon="🎬", layout="centered")

st.markdown("""
<style>
.stApp {
    background-color: #FFF0F5; /* Tatlı pembe arka plan */
}
/* Tüm yazıları koyu renk ve büyük yap */
html, body, [class*="st-"], p, div, label, h1, h2, h3 {
    font-size: 22px !important; 
    font-family: 'Georgia', serif;
    color: #333333 !important; 
}
h1 {
    color: #C71585 !important; /* Başlık rengi */
    text-align: center;
    font-size: 36px !important;
}
/* Buton tasarımı */
.stButton>button {
    width: 100%; 
    border-radius: 15px; 
    font-size: 24px !important;
    font-weight: bold; 
    background-color: #C71585; 
    color: white !important;
    padding: 15px;
}
/* Görselleri ortala ve çerçevele */
img {
    display: block;
    margin-left: auto;
    margin-right: auto;
    width: 80%;
    border-radius: 20px;
    border: 5px solid #C71585;
    box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
}
</style>
""", unsafe_allow_html=True)

st.title("🎬 Yeşilçam Efsane Testi")
st.markdown("### Ruhundaki Jönü veya Sultanı 3 soruda buluyoruz! 💖")
st.markdown("---")

GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

# --- 2. CİNSİYET SEÇİMİ ---
st.markdown("#### Önce bir tanıyalım seni...")
cinsiyet = st.radio("", ["👩 Sultanım (Kadın)", "👨 Jönüm (Erkek)"], horizontal=True)
st.markdown("---")

# --- 3. SORULAR (CİNSİYETE GÖRE DEĞİŞİR) ---
cevaplar = []

if cinsiyet == "👩 Sultanım (Kadın)":
    # --- KADIN SORULARI ---
    s1 = st.radio("1. Pazar sabahı evdeki halin nasıldır? ☀️", [
        "Herkese mükellef bir sofra hazırlarım. (Anaç)",
        "Kahvemi içer, keyfime bakarım. (Zarif)",
        "Hemen işlere girişirim, hamaratım! (Pratik)",
        "Süslenir püslenir, kendime bakarım. (Havalı)"
    ], index=None)
    s2 = st.radio("2. Altın gününde (arkadaş ortamında) sen kimsin? ☕", [
        "Dert dinleyen, akıl veren ablayım.",
        "En şık giyinen ve en asil duranım.",
        "Haksızlığa gelemeyen, lafını esirgemeyenim.",
        "Ortamın neşe kaynağıyım."
    ], index=None)
    s3 = st.radio("3. Hayatta en çok neye önem verirsin? 🌸", [
        "Ailem, yuvam ve sevdiklerim.",
        "Gururum ve duruşum.",
        "Adalet ve dürüstlük.",
        "Sevgi ve neşe."
    ], index=None)
    if s1 and s2 and s3: cevaplar = [s1, s2, s3]

elif cinsiyet == "👨 Jönüm (Erkek)":
    # --- ERKEK SORULARI (YENİ!) ---
    s1 = st.radio("1. Bir haksızlık gördüğünde ne yaparsın? 👊", [
        "Gözümü budaktan sakınmam, dalarım! (Cesur)",
        "Önce uyarır, güzellikle çözmeye çalışırım. (Babacan)",
        "Planımı yapar, akılla çözerim. (Zeki)",
        "Bana dokunmayan yılan bin yaşasın derim. (Rahat)"
    ], index=None)
    s2 = st.radio("2. Aşk hayatında nasıl birisin? 🌹", [
        "Sevdim mi tam severim, gözüm başkasını görmez! (Sadık)",
        "Romantiğimdir, şiirler okur, jestler yaparım. (Duygusal)",
        "Çapkınlık ruhumda var ama belli etmem. (Gizemli)",
        "Kader kısmet der, akışına bırakırım. (Saf)"
    ], index=None)
    s3 = st.radio("3. Arkadaşların senin için ne der? 🤝", [
        "Adam gibi adamdır, sırtın yere gelmez.",
        "Çok yakışıklı ve karizmatiktir.",
        "Biraz saftır ama kalbi tertemizdir.",
        "Sert görünür ama içi pamuk gibidir."
    ], index=None)
    if s1 and s2 and s3: cevaplar = [s1, s2, s3]

st.markdown("---")

# --- 4. SONUÇ BUTONU, GÖRSEL VE YAPAY ZEKA ---
if st.button("✨ Sonucumu Göster ✨"):
    if not cevaplar:
        st.warning("Aman canım, sonucu görmek için tüm soruları cevapla! 🌸")
    else:
        with st.spinner("Arşivler taranıyor, film makaraları dönüyor... 🎞️"):
            try:
                client = genai.Client(api_key=GEMINI_API_KEY)
                
                # Hangi karakter havuzundan seçeceğini belirliyoruz
                if "Kadın" in cinsiyet:
                    havuz = "Türkan Şoray, Fatma Girik, Filiz Akın, Hülya Koçyiğit"
                    resim_kodlari = "TURKAN, FATMA, FILIZ, HULYA"
                else:
                    havuz = "Kadir İnanır, Tarık Akan, Cüneyt Arkın, Kemal Sunal"
                    resim_kodlari = "KADIR, TARIK, CUNEYT, KEMAL"

                prompt = f"""
                GÖREV: Kullanıcı ({cinsiyet}) bir Yeşilçam testi çözdü. Cevapları: {cevaplar}
                Bu cevaplara göre onu şu havuzdan bir karakterle eşleştir: {havuz}
                
                ÇIKTI FORMATI (ÇOK ÖNEMLİ - İKİ SATIR OLACAK):
                SATIR 1: Sadece seçtiğin karakterin resim kodunu yaz ({resim_kodlari} bunlardan biri). Başka hiçbir şey yazma.
                SATIR 2: Facebook postu metnini yaz (Emojili başlık, övücü açıklama, davet cümlesi).
                
                TON: Nostaljik, övücü, sıcak bir Yeşilçam sunucusu gibi konuş.
                """
                
                res = client.models.generate_content(model='gemini-2.5-flash', contents=[prompt])
                
                # Yapay zekadan gelen cevabı "Resim Kodu" ve "Metin" olarak ikiye ayırıyoruz
                tam_cevap = res.text.strip()
                resim_kodu, facebook_metni = tam_cevap.split('\n', 1)
                resim_kodu = resim_kodu.strip()

                # --- GÖRSELİ GÖSTERME KISMI ---
                # Kod ile dosya ismi eşleştirmesi
                resim_haritasi = {
                    "TURKAN": "turkan.jpg", "FATMA": "fatma.jpg", "FILIZ": "filiz.jpg", "HULYA": "hulya.jpg",
                    "KADIR": "kadir.jpg", "TARIK": "tarik.jpg", "CUNEYT": "cuneyt.jpg", "KEMAL": "kemal.jpg"
                }
                
                st.success("İşte Ruhundaki Yeşilçam Efsanesi! 🎉")
                
                # Eğer doğru bir kod geldiyse resmi göster
                if resim_kodu in resim_haritasi:
                    # GitHub'a yüklediğiniz resim dosyasını ekrana basar
                    st.image(resim_haritasi[resim_kodu])
                
                # Metni göster
                st.info(facebook_metni.strip())
                st.markdown("**👇 Sonucunu Facebook'ta paylaş, arkadaşlarını da teste davet et!**")
                
            except Exception as e:
                st.error(f"Hata oluştu (Belki de resim dosyaları eksiktir?): {e}")
