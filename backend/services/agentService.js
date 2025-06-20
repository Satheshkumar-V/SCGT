import axios from 'axios';

export const callInteractionScannerAgent = async (logData) => {
  const response = await axios.post('http://localhost:8000/parse', { logData });
  return response.data;
};

export const callRelationshipQualityAgent = async (parsedInteraction) => {
  const response = await axios.post('http://localhost:8001/evaluate-quality', parsedInteraction);
  return response.data;
};

export const callRelevanceMapperAgent = async (parsedInteraction, goals) => {
  const response = await axios.post('http://localhost:8002/map-relevance', {
    summary: parsedInteraction.summary,
    contact_role: parsedInteraction.role,
    student_goals: goals
  });
  return response.data;
};

export const callReciprocityAgent = async (summary, qualityScore) => {
  const response = await axios.post('http://localhost:8003/check-reciprocity', {
    summary,
    quality_score: qualityScore
  });
  return response.data;
};

export const callSocialCapitalReportAgent = async (interactions, studentName) => {
  const response = await axios.post('http://localhost:8004/generate-okr-report', {
    interactions,
    student_name: studentName
  });
  return response.data;
};