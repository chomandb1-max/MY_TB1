import streamlit as st
from supabase import create_client

# ١. دامەزراندنی پەیوەندی
# دڵنیابە لە دانانی URL و KEYـی خۆت
url ="https://pdgraktldyyvrhqmnqij.supabase.co"
key = "sb_publishable_83vkrjdter6X0Kg-LAiH0g_Q7ingMrv"
supabase = create_client(url, key)

# ٢. فانکشنەکان (Logic)
def get_data():
    return supabase.table("TB1").select("*").execute().data

def add_data(name):
    return supabase.table("TB1").insert({"name": name}).execute()

def update_data(item_id, new_name):
    return supabase.table("TB1").update({"name": new_name}).eq("id", item_id).execute()

def delete_data(item_id):
    return supabase.table("TB1").delete().eq("id", item_id).execute()

# ٣. ڕوکاری مۆبایل (UI)
st.set_page_config(page_title="ئەپی TB1", layout="centered")

with st.sidebar:
    st.title("بەڕێوەبەری ئەپ")
    choice = st.radio("بەشەکان:", ["بینینی داتا", "زیادکردن", "دەستکاری و سڕینەوە"])

# ٤. جێبەجێکردنی بەشەکان
if choice == "بینینی داتا":
    st.subheader("داتاکانی تەیبڵی TB1")
    data = get_data()
    if data:
        st.dataframe(data, use_container_width=True)
    else:
        st.info("هیچ داتایەک نەدۆزرایەوە.")

elif choice == "زیادکردن":
    st.subheader("زیادکردنی ناوی نوێ")
    name = st.text_input("ناو:")
    if st.button("زیادکردن"):
        add_data(name)
        st.success(f"سەرکەوتوو بوو: {name} زیاد کرا!")

elif choice == "دەستکاری و سڕینەوە":
    st.subheader("بەڕێوەبردن")
    item_id = st.number_input("ژمارەی ID:", step=1)
    new_name = st.text_input("ناوی نوێ (بۆ دەستکاری):")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("نوێکردنەوە"):
            update_data(item_id, new_name)
            st.rerun()
    with col2:
        if st.button("سڕینەوە"):
            delete_data(item_id)
            st.rerun()