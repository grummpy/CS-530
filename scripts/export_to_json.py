import json
import os
import sqlite3
from datetime import datetime

def export_all():
    # 1. Fetch chat turns from session database
    db_path = "/Users/daddy/.copilot/session-store.db"
    chat_turns = []
    
    if os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("""
            SELECT turn_index, user_message, assistant_response, timestamp 
            FROM turns 
            WHERE session_id = '69b62c42-9ab8-4d02-8712-d10b8695d3ce'
            ORDER BY turn_index ASC
        """)
        for row in cur.fetchall():
            chat_turns.append({
                "turn_index": row[0],
                "user_message": row[1],
                "assistant_response": row[2],
                "timestamp": row[3]
            })
        conn.close()

    # 2. Collect research documents
    research_files = [
        {
            "id": "ml_hardware_comparative_analysis",
            "title": "Comprehensive Comparative Analysis of Machine Learning Architectures, Prompting Paradigms, and Hardware Substrates in Modern Artificial Intelligence",
            "type": "academic_monograph",
            "path": "research/machine_learning_models_and_hardware_comparative_analysis.md"
        },
        {
            "id": "spartan_ml_field_manual_10th_grade",
            "title": "Spartan-II Machine Learning Field Manual: 10th Grade Edition",
            "type": "educational_field_manual",
            "path": "research/master_chief_ml_bootcamp_10th_grade.md"
        },
        {
            "id": "ml_vs_deep_learning_connection",
            "title": "The Neural Connection: How Machine Learning and Deep Learning Fit Together",
            "type": "conceptual_guide",
            "path": "research/ml_vs_deep_learning_connection.md"
        },
        {
            "id": "home_network_llm_mcp_comparative_analysis",
            "title": "Architectural Comparison & Gap Analysis: Home Network AI Build vs. Theoretical ML Foundations",
            "type": "systems_gap_analysis",
            "path": "research/home_network_llm_mcp_comparative_analysis.md"
        },
        {
            "id": "master_chief_app_system_alignment",
            "title": "Master Chief Hologram: System Architecture & Hardware Alignment Strategy",
            "type": "deployment_blueprint",
            "path": "research/master_chief_app_system_alignment.md"
        }
    ]

    for item in research_files:
        if os.path.exists(item["path"]):
            with open(item["path"], "r", encoding="utf-8") as f:
                item["content"] = f.read()

    # 3. Create combined bundle
    master_bundle = {
        "metadata": {
            "session_id": "69b62c42-9ab8-4d02-8712-d10b8695d3ce",
            "project_name": "CS-530",
            "repository": "grummpy/CS-530",
            "branch": "grummpy-ml-model-background-research",
            "exported_at": datetime.utcnow().isoformat() + "Z",
            "topic": "Machine Learning Research, Prompting Paradigms, Hardware Accelerators, and Local LAN AI Architecture"
        },
        "chat_logs": chat_turns,
        "research_documents": research_files,
        "diagram_manifest": [
            "research/diagrams/ai_ml_dl_nesting_dolls.png",
            "research/diagrams/spartan_ml_radar_clustering.png",
            "research/diagrams/ml_hardware_roofline.png",
            "research/diagrams/master_chief_lan_topology.png",
            "research/diagrams/bland_voice_latency_pipeline.png"
        ]
    }

    # Write unified JSON
    with open("research/research_and_chat_logs.json", "w", encoding="utf-8") as f:
        json.dump(master_bundle, f, indent=2, ensure_ascii=False)
    print("Wrote research/research_and_chat_logs.json")

    # Write separate chat logs JSON
    chat_bundle = {
        "metadata": master_bundle["metadata"],
        "turns_count": len(chat_turns),
        "chat_logs": chat_turns
    }
    with open("docs/chat_logs/chat_logs.json", "w", encoding="utf-8") as f:
        json.dump(chat_bundle, f, indent=2, ensure_ascii=False)
    print("Wrote docs/chat_logs/chat_logs.json")

    # Write separate research corpus JSON
    research_bundle = {
        "metadata": master_bundle["metadata"],
        "document_count": len(research_files),
        "documents": research_files
    }
    with open("research/research_corpus.json", "w", encoding="utf-8") as f:
        json.dump(research_bundle, f, indent=2, ensure_ascii=False)
    print("Wrote research/research_corpus.json")

if __name__ == "__main__":
    export_all()
