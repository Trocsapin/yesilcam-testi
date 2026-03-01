import streamlit as st
from google import genai
import random
import urllib.parse 

# ==========================================
# AYAR: SİTE LİNKİ
# ==========================================
SITENIZIN_LINKI = "https://yesilcam-testi.streamlit.app/"

# ==========================================
# PART 1: ULTRA ALBENİLİ VE MOBİL UYUMLU TASARIM
# ==========================================
st.set_page_config(page_title="Yeşilçam Eğlence Merkezi", page_icon="🎬", layout="centered")

st.markdown("""
<style>
.stApp { background: radial-gradient(circle, #2c0e2c 0%, #1a051a 100%); color: #ffe0b3 !important; }
html, body, [class*="st-"], p, div, label { font-size: 20px !important; font-family: 'Georgia', serif; color: #ffe0b3 !important; }
h1 { color: #ff3399 !important; text-align: center; font-size: 40px !important; font-weight: bold; text-shadow: 0 0 10px #ff3399, 0 0 20px #ff3399; margin-bottom: 20px; }
h2, h3, h4 { color: #ff3399 !important; text-align: center; }

/* SEKMELER */
div[data-baseweb="tab-list"] { gap: 5px; }
button[data-baseweb="tab"] { background-color: #4d0026 !important; color: #ffe0b3 !important; border-radius: 10px !important; border: 2px solid #ff3399 !important; padding: 10px 15px !important; font-size: 20px !important; font-weight: bold !important; white-space: normal !important; }
button[data-baseweb="tab"][aria-selected="true"] { background: linear-gradient(180deg, #ff3399 0%, #ff0066 100%) !important; color: white !important; border: 2px solid white !important; box-shadow: 0 0 15px #ff3399; }

/* MOBİL UYUM */
@media (max-width: 768px) {
    div[data-baseweb="tab-list"] { flex-direction: column !important; width: 100% !important; }
    button[data-baseweb="tab"] { width: 100% !important; margin-bottom: 10px !important; border-radius: 15px !important; padding: 15px !important; font-size: 22px !important; }
}

/* BUTONLAR */
.stButton>button { width: 100%; border-radius: 20px; font-size: 26px !important; font-weight: bold; background: linear-gradient(180deg, #ffcc00 0%, #ff9900 100%); color: #33001a !important; border: 4px solid #ffe0b3; padding: 15px; box-shadow: 0 5px 15px rgba(255, 204, 0, 0.4); transition: all 0.3s ease; }
.stButton>button:hover { transform: scale(1.03); }

/* RESİMLER */
img { display: block; margin-left: auto; margin-right: auto; width: 90%; border-radius: 15px; border: 8px solid #ffe0b3; box-shadow: 0 10px 25px rgba(0, 0, 0, 0.7); margin-top: 20px; margin-bottom: 20px; }

/* KUTULAR */
.stAlert { background-color: #33001a !important; border: 2px solid #ff3399 !important; border-radius: 15px; color: #ffe0b3 !important; }

/* PAYLAŞ BUTONLARI İÇİN ÖZEL TASARIM */
.share-btn { display: inline-block; width: 48%; text-align: center; padding: 12px; border-radius: 10px; font-weight: bold; font-size: 18px; text-decoration: none !important; margin-top: 10px; color: white !important; }
.fb-btn { background-color: #1877F2; border: 2px solid #0d5bb5; }
.wa-btn { background-color: #25D366; border: 2px solid #1da851; float: right; }
@media (max-width: 768px) { .share-btn { width: 100%; float: none; margin-bottom: 10px; font-size: 20px; padding: 15px; } }
</style>
""", unsafe_allow_html=True)

st.title("🎬 Yeşilçam Eğlence Merkezi")
st.markdown("<h3 style='text-align: center; color: #ffe0b3;'>Melek mi, Şeytan mı? Gerçek yüzünü bulmaya hazır mısın? 💖</h3>", unsafe_allow_html=True)
st.markdown("---")

GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

# ==========================================
# PART 2: YENİ, PSİKOLOJİK VE GERÇEKÇİ SORU HAVUZLARI
# ==========================================
jon_sultan_pool = [
    {"q": "Mahalleden biri arkandan atıp tutmuş, kulağına geldi. Ne yaparsın? 👂", "c": ["Yüzüne gülerim ama defterini sonsuza kadar dürmüşümdür. (Sinsi/Gururlu)", "Gider kapısına dayanır, 'Hayırdır inşallah?' diye hesap sorarım. (Dobra/Agresif)", "Hiç bozuntuya vermem, altın gününde lafı gediğine oturturum. (Zarif intikam)", "Umursamam ama içten içe günlerce kafama takar, sinir olurum. (Alıngan)"]},
    {"q": "Aile içinde (veya gelin/damat/elti ile) bir şeye çok gıcık oldun. Tepkin ne olur? 🙄", "c": ["Surat asarım, buz gibi davranırım, tavrımdan anlasınlar. (Pasif-Agresif)", "Laf sokarım, anlarsa anlar, anlamazsa kendi bilir. (İğneleyici)", "Hiçbir şey demem ama gidip başkasına şikayet ederim. (Dedikoducu)", "Çat diye söylerim, içimde patlayacağına onda dert olsun. (Patavatsız)"]},
    {"q": "Evde kimsenin pek bilmediği, en belirgin gizli huyun nedir? 🤫", "c": ["Her şey benim dediğim gibi olsun isterim, kontrolcüyüm.", "Kin tutarım, yapılan hatayı yıllar geçse de unutmam, yüzüne vururum.", "Dışarıdan sakin görünürüm ama kafamda hep senaryolar yazarım.", "Saman alevi gibiyimdir, aniden parlar ortalığı yıkarım, 5 dakika sonra pamuk gibi olurum."]},
    {"q": "Yakın bir arkadaşın senden daha lüks/güzel bir şey aldı. İlk tepkin ne olur? 💎", "c": ["Güle güle kullansın derim ama içimden 'Keşke benim olsaydı' diye geçiririm.", "Hemen neresinde bir kusur var diye incelemeye başlarım.", "'Aman canım benimkiler bana yeter' diyerek kendimi avuturum.", "Hırs yaparım, en kısa zamanda aynısından veya daha iyisinden alırım."]}
]

kotu_komedi_pool = [
    {"q": "Kabul et, bazen kötü olmak çok zevkli! Yeşilçam'da bir kötü olsaydın imza hareketin ne olurdu? 😈", "c": ["Gözlerimi kısarak sinsi sinsi gülmek ve başkalarının kuyusunu kazmak.", "Gazozuna ilacı atıp (veya dedikoduyla) safları tuzağa düşürmek.", "Masaya yumruğu vurup 'Bu evlilik ASLA olmayacak!' diyerek ortalığı karıştırmak.", "Parayla herkesi ve her şeyi satın alabileceğimi düşünerek kibirle tepeden bakmak."]},
    {"q": "Mahallede büyük bir kavga koptu ve aslında sen haksızsın. İşin içinden nasıl sıyrılırsın? 🎭", "c": ["Laf cambazlığıyla üste çıkar, haklıyı haksız duruma düşürürüm.", "Hemen acındırma politikası yapar, anında mağduru oynarım.", "Hiç çaktırmadan 'Ben yapmadım ki, o başlattı' diyerek suçu başkasına atarım.", "Umurumda bile olmaz, 'Yaptım, yine olsa yine yaparım!' der geçerim."]},
    {"q": "Gıcık olduğun biri yolda ayağı takılıp düştü. İçinden ne geçer? 🤭", "c": ["Zar zor gülmemi tutarım, içimden 'İlahi adalet işte' derim.", "Gidip 'Ayy canım iyi misin?' derim ama aslında düşmesine bayılmışımdır.", "Gözünün içine baka baka kahkahayı patlatırım.", "Ben düşürmedim ama düşsün diye içimden geçirmiş olabilirim."]}
]

replik_fali_pool = [
    {"r": "Benim adım Tatar Ramazan, ben bu oyunu bozarım!", "t": "Bugün önüne engeller çıkabilir. Dikkatli ol ama taviz verme."},
    {"r": "Sevgi neydi? Sevgi emekti.", "t": "Bugün ilişkilerinde sabırlı olman, emek vermen gerekecek."},
    {"r": "Bedenime sahip olabilirsin ama ruhuma asla!", "t": "Bugün birileri seni zorlayabilir. Duruşunu bozma, iç dünyanı koru."}
]

# ==========================================
# PAYLAŞIM BUTONLARI
# ==========================================
def paylasim_butonlari_olustur(metin):
    hazir_mesaj = f"{metin}\n\nSen hangi efsanesin? Hemen testi çöz: {SITENIZIN_LINKI}"
    encoded_mesaj = urllib.parse.quote(hazir_mesaj)
    encoded_url = urllib.parse.quote(SITENIZIN_LINKI)
    
    fb_link = f"https://www.facebook.com/sharer/sharer.php?u={encoded_url}&quote={encoded_mesaj}"
    wa_link = f"https://api.whatsapp.com/send?text={encoded_mesaj}"
    
    st.markdown(f"""
        <div style="margin-top: 20px; margin-bottom: 20px;">
            <a href="{fb_link}" target="_blank" class="share-btn fb-btn">📘 Facebook'ta Paylaş</a>
            <a href="{wa_link}" target="_blank" class="share-btn wa-btn">🟩 WhatsApp'tan Gönder</a>
            <div style="clear: both;"></div>
        </div>
    """, unsafe_allow_html=True)

# ==========================================
# PART 3: SEKME SİSTEMİ
# ==========================================
tab1, tab2, tab3 = st.tabs(["🎭 Ruhundaki Jön/Sultan", "🦹‍♂️ Kötüler ve Komedyenler", "🥠 Günlük Replik Falı"])

with tab1:
    st.markdown("<h3 style='text-align: center; color: #ffe0b3;'>Gerçek Yüzünle Efsanevi Bir Kahraman Mısın?</h3>", unsafe_allow_html=True)
    cinsiyet = st.radio("Önce bir tanıyalım seni...", ["👩 Sultanım (Kadın)", "👨 Jönüm (Erkek)"], horizontal=True, key="cinsiyet_1")
    
    if 'selected_questions_1' not in st.session_state: st.session_state['selected_questions_1'] = random.sample(jon_sultan_pool, 3)
    
    cevaplar_1 = []
    for i, q in enumerate(st.session_state['selected_questions_1']):
        c = st.radio(q["q"], q["c"], index=None, key=f"q1_{i}")
        if c: cevaplar_1.append(c)

    st.markdown("---")
    if st.button("✨ Sonucumu Göster ✨", key="btn_1"):
        if not cevaplar_1: st.warning("Aman canım, sonucu görmek için tüm soruları cevapla! 🌸")
        else:
            with st.spinner("Arşivler taranıyor, film makaraları dönüyor... 🎞️"):
                try:
                    client = genai.Client(api_key=GEMINI_API_KEY)
                    havuz = "Türkan Şoray, Fatma Girik, Filiz Akın, Hülya Koçyiğit" if "Kadın" in cinsiyet else "Kadir İnanır, Tarık Akan, Cüneyt Arkın, Kemal Sunal"
                    resim_kodlari = "TURKAN, FATMA, FILIZ, HULYA" if "Kadın" in cinsiyet else "KADIR, TARIK, CUNEYT, KEMAL"

                    prompt = f"Kullanıcı ({cinsiyet}) gerçekçi ve hafif kusurlu şıkların olduğu bir Yeşilçam testi çözdü. Cevapları: {cevaplar_1}. Onu bu psikolojik cevaplarına göre {havuz} havuzundan biriyle eşleştir.\nTON: Nostaljik Yeşilçam sunucusu gibi, onun o kusurlu/harbi yanını hafif mizahi bir dille öv.\nSATIR 1: Sadece ve sadece resim kodunu yaz ({resim_kodlari}). Başka kelime ekleme.\nSATIR 2: Sosyal medya metni."
                    res = client.models.generate_content(model='gemini-2.5-flash', contents=[prompt])
                    
                    resim_kodu_ham, facebook_metni = res.text.strip().split('\n', 1)
                    resim_kodu_ham = resim_kodu_ham.upper()
                    
                    jon_sultan_links = {
                        "TURKAN": "https://i.pinimg.com/736x/a2/df/a3/a2dfa35e0257324ce218254d84b32edc.jpg",
                        "FATMA": "https://i.pinimg.com/736x/8b/19/f4/8b19f4a574fac6f52e3854f2a060a857.jpg",
                        "FILIZ": "https://i.pinimg.com/736x/a0/20/44/a02044b48d9db9d5014771398b985493.jpg",
                        "HULYA": "https://i.pinimg.com/736x/27/1f/88/271f88d8bba07d94118e51585e74ad92.jpg",
                        "KADIR": "https://i.pinimg.com/736x/1c/15/ba/1c15ba970ee745a0493906c83b6e153b.jpg",
                        "TARIK": "https://i.pinimg.com/1200x/86/58/6a/86586ae7f9e912bf9247fca2b6be3724.jpg",
                        "CUNEYT": "https://i.pinimg.com/736x/c2/b4/cc/c2b4cc0733f8e40cd62935d79415c1e6.jpg",
                        "KEMAL": "https://i.pinimg.com/736x/a5/8f/3f/a58f3f23c551da185babe810db58bdf8.jpg"
                    }
                    
                    bulunan_kod = None
                    for k in jon_sultan_links.keys():
                        if k in resim_kodu_ham:
                            bulunan_kod = k
                            break
                    
                    st.success("İşte Ruhundaki Yeşilçam Efsanesi! 🎉")
                    if bulunan_kod:
                        try: st.image(jon_sultan_links[bulunan_kod])
                        except: pass
                    
                    st.info(facebook_metni.strip())
                    paylasim_butonlari_olustur(facebook_metni.strip())
                    del st.session_state['selected_questions_1']
                except Exception as e: st.error("Bir takılma oldu, lütfen tekrar dene!")

with tab2:
    st.markdown("<h3 style='text-align: center; color: #ffe0b3;'>Gazozuna İlaç Atan Mı, Herkesi Güldüren Mi?</h3>", unsafe_allow_html=True)
    kategori_2 = st.radio("İçindeki hangi gücü keşfetmek istersin?", ["👿 İçimdeki Kötü Karakter", "😂 Komedi Efsanesi"], horizontal=True, key="kategori_2")
    
    if 'selected_questions_2' not in st.session_state: st.session_state['selected_questions_2'] = random.sample(kotu_komedi_pool, 2)
    
    cevaplar_2 = []
    for i, q in enumerate(st.session_state['selected_questions_2']):
        c = st.radio(q["q"], q["c"], index=None, key=f"q2_{i}")
        if c: cevaplar_2.append(c)

    st.markdown("---")
    if st.button("👿 Ruhumdaki Karakteri Göster 😂", key="btn_2"):
        if not cevaplar_2: st.warning("Lütfen tüm soruları cevapla!")
        else:
            with st.spinner("Sinsi planlar/kahkahalar taranıyor... 🎞️"):
                try:
                    client = genai.Client(api_key=GEMINI_API_KEY)
                    havuz = "Erol Taş, Nuri Alço, Aliye Rona, Önder Somer" if "Kötü" in kategori_2 else "Adile Naşit, Şener Şen, Münir Özkul, Kemal Sunal"
                    resim_kodlari = "EROL, NURI, ALIYE, ONDER" if "Kötü" in kategori_2 else "ADILE, SENER, MUNIR, KEMAL"

                    prompt = f"Kategori: {kategori_2}. Cevapları: {cevaplar_2}. {havuz} havuzundan seç.\nSATIR 1: Sadece ve sadece resim kodunu yaz ({resim_kodlari}). Başka kelime ekleme.\nSATIR 2: Sosyal medya metni."
                    res = client.models.generate_content(model='gemini-2.5-flash', contents=[prompt])
                    
                    resim_kodu_ham, facebook_metni = res.text.strip().split('\n', 1)
                    resim_kodu_ham = resim_kodu_ham.upper()
                    
                    kotu_komedi_links = {
                        "EROL": "https://i.pinimg.com/736x/5b/29/19/5b29199f8d9848a6c91cb931c6d12fd4.jpg",
                        "NURI": "https://i.pinimg.com/736x/60/f4/b9/60f4b91d2927111f3feb64f705b7f10c.jpg",
                        "ALIYE": "https://i.pinimg.com/736x/8a/6b/0c/8a6b0c445a325b83170b025a3e9a116a.jpg",
                        "ONDER": "https://i.pinimg.com/1200x/1c/a9/50/1ca950e45eb1b5b8ae5ef05529d8cac5.jpg",
                        "ADILE": "https://i.pinimg.com/736x/6c/5c/f4/6c5cf45c657fe414d89cdfdfe0894694.jpg",
                        "SENER": "https://i.pinimg.com/736x/4d/06/4a/4d064aa29c91493109945dc42619d12b.jpg",
                        "MUNIR": "https://i.pinimg.com/736x/06/3f/cb/063fcb34e08f1b279bde0bfe63887e16.jpg",
                        "KEMAL": "https://i.pinimg.com/736x/a5/8f/3f/a58f3f23c551da185babe810db58bdf8.jpg"
                    }
                    
                    bulunan_kod = None
                    for k in kotu_komedi_links.keys():
                        if k in resim_kodu_ham:
                            bulunan_kod = k
                            break
                            
                    st.success("İşte Ruhundaki Yeşilçam Karakteri! 🎉")
                    if bulunan_kod:
                        try: st.image(kotu_komedi_links[bulunan_kod])
                        except: pass
                    
                    st.info(facebook_metni.strip())
                    paylasim_butonlari_olustur(facebook_metni.strip())
                    del st.session_state['selected_questions_2']
                except Exception as e: st.error("Bir takılma oldu, lütfen tekrar dene!")

with tab3:
    st.markdown("<h3 style='text-align: center; color: #ffe0b3;'>Bugün Film Makaraları Senin İçin Ne Diyor?</h3>", unsafe_allow_html=True)
    if st.button("🥠 Bugünkü Yeşilçam Falımı Çek 🥠", key="btn_falcibaci"):
        with st.spinner("Film makaraları dönüyor... 🎞️"):
            secilen_fal = random.choice(replik_fali_pool)
            fal_metni = f"💬 \"{secilen_fal['r']}\"\n\n✨ Tavsiyen: {secilen_fal['t']}"
            
            st.markdown(f"""
            <div style='background-color: #33001a; border: 4px solid #ffcc00; border-radius: 20px; padding: 25px; box-shadow: 0 10px 20px rgba(0,0,0,0.5);'>
                <h2 style='color: #ffcc00 !important; font-style: italic; font-size: 30px !important; margin-bottom: 20px;'>💬 "{secilen_fal["r"]}"</h2>
                <hr style='border: 1px solid #ff3399;'>
                <p style='color: #ffe0b3 !important; font-size: 22px !important; line-height: 1.5;'>✨ Bugünkü Tavsiyen:</p>
                <p style='color: white !important; font-size: 24px !important; font-weight: bold;'>{secilen_fal["t"]}</p>
            </div>
            """, unsafe_allow_html=True)
            
            paylasim_butonlari_olustur(f"Bugünkü Yeşilçam Falımı çektim:\n{fal_metni}")
