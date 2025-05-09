import streamlit as st
import requests


GROUP_COLORS = {
    "ORG": "#FF6B6B",
    "PER": "#4ECDC4",
    "LOC": "#FFD93D",
    "MISC": "#AC66CC"
}

GROUP_ICONS = {
    "ORG": "🏢",
    "PER": "👤",
    "LOC": "🌍",
    "MISC": "📌"
}

group_labels = {
    "ORG": "Organizations",
    "PER": "People",
    "LOC": "Locations",
    "MISC": "Miscellaneous"
}


def reset_form():
    """Reset all form data and analysis results"""
    st.session_state.text_input = ""
    st.session_state.analysis_results = None
    st.session_state.input_text = ""
    


st.title("📄 Named Entity Recognition (NER) Application")

with st.expander("ℹ️ Project Information & Usage Guide", expanded= False):
    st.markdown(f"""
    ### About This Project
    This application performs Named Entity Recognition (NER) using a pre-trained BERT model. 
    It identifies entities such as persons, organizations, locations, and more in the given text.


    ### 📌 Comprehensive Guide
    
    ### 🌟 Key Features
    - **Smart Entity Recognition**: {GROUP_ICONS['PER']} People, {GROUP_ICONS['ORG']} Organizations
    - **Context Awareness**: {GROUP_ICONS['LOC']} Location context analysis
    - **Confidence Visualization**: Color-coded accuracy indicators
    - **Multi-word Support**: Hyphenated entity merging

    
    ### 🛠️ Technical Stack
    | Component       | Technology               |
    |-----------------|--------------------------|
    | **AI Model**    | `dslim/bert-base-NER`    |
    | **Backend**     | Flask REST API           |
    | **Frontend**    | Streamlit                |
    | **Processing**  | Hugging Face Transformers|

    ### ⚙️️ **How to Use**:
    1. 📥 Enter text in the input box below  
    2. 🔍 Click 'Analyze' to process the text  
    3. 📊 View results in categorized sections  
    4. 🧹 Use 'Clear' to reset the input

    
    ### 📝 Best Practices
    {GROUP_ICONS['PER']} **People Detection**  
    - Use *O'Neil* instead of *O'neil* (space after apostrophe)  
    - Write *ElonMusk* instead of *Elon-Musk* (avoid hyphens)
    
    {GROUP_ICONS['LOC']} **Location Tips**  
    - For cities like *NewYork*, avoid hyphens
    - Use common spelling variants
    
    ### ⚠️ Known Limitations
    1. Maximum text length: ~500 characters
    2. Rare entity types may show lower confidence
    3. Context-dependent classification
    """)


col1, col2 = st.columns([1, 3])
with col1:
    analyze_clicked = st.button("Analyze")
with col2:
    if st.button("Clear"):
        reset_form()




text = st.text_area(
    "Enter text to analyze:", 
    height=150, 
    value=st.session_state.get("input_text", ""),
    key="text_input"  
)

if analyze_clicked:
    if not text.strip():
        st.warning("Please enter some text.")
    else:
        st.session_state.analysis_results = None
        st.session_state.input_text = text  
        with st.spinner("Analyzing text..."):
            try:
                response = requests.post(
                    "http://localhost:5000/analyze",
                    json={"text": text},
                    timeout=30
                )
                
                if response.status_code == 200:
                    entities = response.json()
                    
                     
                  
                     
                    entities_dict = {}
                    for ent in entities:
                        group = ent["entity_group"]
                        entities_dict.setdefault(group, []).append(ent)
                    
                    st.markdown("### Analysis Results ")
                    st.markdown("---")
                    cols = st.columns(4)
                    counts = {g: len(entities_dict.get(g, [])) for g in GROUP_COLORS}
                    
                    for i, group in enumerate(GROUP_COLORS):
                        cols[i].markdown(f"""
                        <div style="
                            background: {GROUP_COLORS[group]}10;
                            border-radius: 10px;
                            padding: 15px;
                            border-left: 4px solid {GROUP_COLORS[group]};
                            margin: 10px 0;
                        ">
                            <h3 style="color: {GROUP_COLORS[group]}; margin:0;">
                                {GROUP_ICONS[group]} {counts[group]}
                            </h3>
                            <small>{group_labels[group]}</small>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    
                    with st.expander("🔍 Full Entity List", expanded= False):
                        group_order = ["PER", "ORG", "LOC", "MISC"]
                        
                        for group in group_order:
                            if group in entities_dict:
                                st.markdown(f"""
                                <div style="
                                    background: {GROUP_COLORS[group]}20;
                                    padding: 10px;
                                    border-radius: 5px;
                                    margin: 10px 0;
                                ">
                                    <h4 style="color: {GROUP_COLORS[group]}; margin:0;">
                                        {GROUP_ICONS[group]} {group_labels[group]} ({len(entities_dict[group])})
                                    </h4>
                                </div>
                                """, unsafe_allow_html=True)
                                
                                for ent in entities_dict[group]:
                                    confidence_bar = f"""
                                    <div style="
                                        width: 100%;
                                        height: 4px;
                                        background: {GROUP_COLORS[group]}30;
                                        border-radius: 2px;
                                        margin-top: 2px;
                                    ">
                                        <div style="
                                            width: {ent['score']*100}%;
                                            height: 100%;
                                            background: {GROUP_COLORS[group]};
                                            border-radius: 2px;
                                        "></div>
                                    </div>
                                    """
                                    
                                    st.markdown(f"""
                                    <div style="
                                        padding: 8px;
                                        margin: 4px 0;
                                        border-left: 3px solid {GROUP_COLORS[group]};
                                    ">
                                        <div style="display: flex; justify-content: space-between;">
                                            <div>
                                                <strong>{ent['word']}</strong>
                                                <div style="font-size:0.8em; color:#666">
                                                    Position: {ent['start']}-{ent['end']}
                                                </div>
                                            </div>
                                            <div style="color: {GROUP_COLORS[group]}; font-weight: bold;">
                                                {ent['score']*100:.0f}%
                                            </div>
                                        </div>
                                        {confidence_bar}
                                    </div>
                                    """, unsafe_allow_html=True)
                
                else:
                    st.error(f"API request failed. Status code: {response.status_code}")
                    
            except requests.exceptions.RequestException as e:
                st.error(f"Connection error: {str(e)}")
