import streamlit as st
from google import genai

# --- 1. HERKES İÇİN NOSTALJİK TASARIM ---
st.set_page_config(page_title="Yeşilçam Efsane Testi", page_icon="🎬", layout="centered")

st.markdown("""
<style>
.stApp { background-color: #FFF0F5; }
html, body, [class*="st-"], p, div, label, h1, h2, h3 {
    font-size: 22px !important; 
    font-family: 'Georgia', serif;
    color: #333333 !important; 
}
h1 {
    color: #C71585 !important;
    text-align: center;
    font-size: 36px !important;
}
.stButton>button {
    width: 100%; 
    border-radius: 15px; 
    font-size: 24px !important;
    font-weight: bold; 
    background-color: #C71585; 
    color: white !important;
    padding: 15px;
}
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

cevaplar = []

if cinsiyet == "👩 Sultanım (Kadın)":
    s1 = st.radio("1. Pazar sabahı evdeki halin nasıldır? ☀️", [
        "Herkese mükellef bir sofra hazırlarım. (Anaç)",
        "Kahvemi içer, keyfime bakarım. (Zarif)",
        "Hemen işlere girişirim, hamaratım! (Pratik)",
        "Süslenir püslenir, kendime bakarım. (Havalı)"
    ], index=None)
    s2 = st.radio("2. Altın gününde sen kimsin? ☕", [
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

if st.button("✨ Sonucumu Göster ✨"):
    if not cevaplar:
        st.warning("Aman canım, sonucu görmek için tüm soruları cevapla! 🌸")
    else:
        with st.spinner("Arşivler taranıyor, film makaraları dönüyor... 🎞️"):
            try:
                client = genai.Client(api_key=GEMINI_API_KEY)
                
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
                
                tam_cevap = res.text.strip()
                resim_kodu, facebook_metni = tam_cevap.split('\n', 1)
                resim_kodu = resim_kodu.strip()

                # --- İŞTE YENİ LİNK SİSTEMİ (İNDİRME YOK!) ---
                # İnternetten kopyaladığınız resim adreslerini aşağıdaki tırnakların içine yapıştırın
                resim_haritasi = {
                    "TURKAN": "https://i.pinimg.com/736x/a2/df/a3/a2dfa35e0257324ce218254d84b32edc.jpg",
                    "FATMA": "https://i.pinimg.com/736x/8b/19/f4/8b19f4a574fac6f52e3854f2a060a857.jpg",
                    "FILIZ": "https://i.pinimg.com/736x/a0/20/44/a02044b48d9db9d5014771398b985493.jpg",
                    "HULYA": "https://i.pinimg.com/736x/27/1f/88/271f88d8bba07d94118e51585e74ad92.jpg",
                    "KADIR": "https://i.pinimg.com/736x/1c/15/ba/1c15ba970ee745a0493906c83b6e153b.jpg",
                    "TARIK": "https://i.pinimg.com/1200x/86/58/6a/86586ae7f9e912bf9247fca2b6be3724.jpg",
                    "CUNEYT": "https://i.pinimg.com/736x/c2/b4/cc/c2b4cc0733f8e40cd62935d79415c1e6.jpg",
                    "KEMAL": "https://i.pinimg.com/736x/a5/8f/3f/a58f3f23c551da185babe810db58bdf8.jpg"
                }
                
                st.success("İşte Ruhundaki Yeşilçam Efsanesi! 🎉")
                
                # İnternetteki linkten fotoğrafı doğrudan ekrana basıyoruz
                if resim_kodu in resim_haritasi:
                    try:
                        st.image(resim_haritasi[resim_kodu])
                    except:
                        st.warning("Görsel yüklenemedi. Lütfen koda eklediğiniz resim linkini kontrol edin.")
                
                st.info(facebook_metni.strip())
                st.markdown("**👇 Sonucunu Facebook'ta paylaş, arkadaşlarını da teste davet et!**")
                
            except Exception as e:
                st.error(f"Sistemde ufak bir takılma oldu: {e}")
