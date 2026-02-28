import streamlit as st
from supabase import create_client
import os

# پەیوەندیکردن بە سوپابەیس بە بەکارهێنانی Secrets
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

# دیزاینی ڕوکار
st.set_page_config(page_title="سیستەمی TB1", layout="centered")

# فانکشنەکان
def get_data():
    return supabase.table("TB1").select("*").execute().data

# مێنوی سەرەکی
with st.sidebar:
    st.title("⚙️ بەڕێوەبەری ئەپ")
    choice = st.radio("بەشەکان:", ["بینین و سێرچ", "زیادکردن", "بەڕێوەبردن"])

# بەشی بینین و سێرچ
if choice == "بینین و سێرچ":
    st.subheader("📊 داتاکانی TB1")
    data = get_data()
    
    if data:
        # ژماردنی کۆی بەشداربووان
        st.metric(label="کۆی بەشداربووان", value=len(data))
        
        # بەشی سێرچ
        search = st.text_input("🔍 گەڕان بەدوای ناوێکدا...")
        if search:
            filtered = [item for item in data if search.lower() in item['name'].lower()]
            st.dataframe(filtered, use_container_width=True)
        else:
            st.dataframe(data, use_container_width=True)
    else:
        st.info("هیچ داتایەک نەدۆزرایەوە.")

# بەشی زیادکردن
elif choice == "زیادکردن":
    st.subheader("➕ زیادکردنی ناوی نوێ")
    new_name = st.text_input("ناو بنووسە:")
    if st.button("تۆمارکردن"):
        supabase.table("TB1").insert({"name": new_name}).execute()
        st.success("بە سەرکەوتوویی زیاد کرا! ✅")

# بەشی بەڕێوەبردن (سڕینەوە)
elif choice == "بەڕێوەبردن":
    st.subheader("🗑️ سڕینەوە و دەستکاری")
    item_id = st.number_input("ژمارەی ID:", step=1)
    
    if st.button("سڕینەوەی ئەم IDـیە"):
        supabase.table("TB1").delete().eq("id", item_id).execute()
        st.warning("بەشداربووەکە سڕایەوە.")
        st.rerun()