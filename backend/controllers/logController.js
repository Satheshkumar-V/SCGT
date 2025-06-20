import Interaction from '../models/Interaction.js';
import {
  callInteractionScannerAgent,
  callRelationshipQualityAgent,
  callRelevanceMapperAgent,
  callReciprocityAgent
} from '../services/agentService.js';

export const handleLogUpload = async (req, res) => {
  try {
    const { logData, studentGoals } = req.body;
    if (!logData || !studentGoals) return res.status(400).json({ error: 'logData and studentGoals required' });

    // Agent 1
    const parsed = await callInteractionScannerAgent(logData);

    // Agent 2
    const quality = await callRelationshipQualityAgent({ summary: parsed.summary });

    // Agent 3
    const relevance = await callRelevanceMapperAgent(parsed, studentGoals);

    const reciprocity = await callReciprocityAgent(parsed.summary, quality.quality_score);

const newInteraction = new Interaction({
  // Existing fields ...
  relevanceScore: relevance.relevance_score,
  contactAlignment: relevance.contact_alignment,
  contentRelevance: relevance.content_relevance,
  goalMatchReasoning: relevance.goal_synergy_reasoning,

  reciprocityStatus: reciprocity.reciprocity_status,
  reciprocityEvidence: reciprocity.evidence
});

    await newInteraction.save();
    res.json({ success: true, data: newInteraction });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Failed to process interaction' });
  }
};

export const getAllInteractions = async (req, res) => {
  try {
    const interactions = await Interaction.find().sort({ createdAt: -1 });
    res.json(interactions);
  } catch (err) {
    res.status(500).json({ error: 'Error fetching interactions' });
  }
};
