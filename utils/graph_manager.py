import networkx as nx
from pyvis.network import Network
import streamlit.components.v1 as components
import os
import re

class GraphManager:
    def __init__(self):
        self.graph = nx.DiGraph()
        self._initialize_base_knowledge()

    def _initialize_base_knowledge(self):
        # Base medical knowledge
        base_relations = [
            ("Dengue", "Fever", "causes symptom"),
            ("Dengue", "Paracetamol", "treated with"),
            ("Diabetes", "High Blood Sugar", "characterized by"),
            ("Diabetes", "Insulin", "managed with"),
            ("Hypertension", "Dizziness", "symptom"),
            ("COVID-19", "Cough", "symptom")
        ]
        for src, dst, rel in base_relations:
            self.add_relationship(src, rel, dst)

    def add_relationship(self, entity1, relation, entity2):
        self.graph.add_edge(entity1, entity2, label=relation)

    def extract_from_text(self, text, llm=None):
        """
        Extracts relationships using LLM or simple heuristics.
        """
        if llm:
            try:
                extraction_prompt = f"Extract medical relationships in the format 'Entity1 -> Relation -> Entity2' from the following text. Limit to 5 key relationships: \n\n{text[:2000]}"
                response = llm.invoke(extraction_prompt).content
                # Simple parsing of 'A -> B -> C'
                lines = response.split('\n')
                for line in lines:
                    if '->' in line:
                        parts = line.split('->')
                        if len(parts) == 3:
                            self.add_relationship(parts[0].strip(), parts[1].strip(), parts[2].strip())
            except Exception as e:
                print(f"Error extracting graph relations: {e}")

    def generate_graph_html(self, path="graph.html"):
        net = Network(height="480px", width="100%", bgcolor="#0E1117", font_color="#E0E0E0", directed=True)
        
        # Color palette
        node_colors = ["#1E88E5", "#D81B60", "#43A047", "#FB8C00", "#5E35B1"]
        
        # Customize nodes
        for i, node in enumerate(self.graph.nodes()):
            color = node_colors[i % len(node_colors)]
            net.add_node(node, label=node, color=color, font={'size': 20, 'color': 'white'})
            
        # Customize edges
        for edge in self.graph.edges(data=True):
            net.add_edge(edge[0], edge[1], label=edge[2].get('label', ''), color="#546E7A", arrows="to")

        net.set_options("""
        var options = {
          "physics": {
            "barnesHut": {
              "gravitationalConstant": -1000,
              "centralGravity": 0.5,
              "springLength": 80
            },
            "minVelocity": 0.75,
            "stabilization": { "enabled": true, "iterations": 100 }
          },
          "interaction": {
            "zoomView": false,
            "dragView": false,
            "dragNodes": true
          }
        }
        """)
        net.save_graph(path)
        return path
    def visualize(self):
        path = self.generate_graph_html()
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                html = f.read()
            return html
        return "<p>Graph visualization failed.</p>"
    
