from tools.interaction_scanner import extract_interactions_from_log
from tools.relationship_evaluator import evaluate_relationship_quality
from tools.relevance_mapper import map_relevance_to_goals
from tools.reciprocity_detector import detect_reciprocity
from tools.report_generator import generate_report

def run_pipeline(logs: List[str], student_goals: List[str]):
    interaction_data = [extract_interactions_from_log(log) for log in logs]
    quality_scores = [evaluate_relationship_quality(i) for i in interaction_data]
    relevance_scores = [map_relevance_to_goals(i, student_goals) for i in interaction_data]
    reciprocity_data = [detect_reciprocity(i, q) for i, q in zip(interaction_data, quality_scores)]
    report = generate_report(interaction_data, quality_scores, relevance_scores, reciprocity_data)
    return report
