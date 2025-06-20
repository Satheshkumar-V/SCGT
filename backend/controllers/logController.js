import Interaction from '../models/Interaction.js';
import { callInteractionScannerAgent } from '../services/agentService.js';

export const handleLogUpload = async (req, res) => {
  try {
    const { logData } = req.body;

    if (!logData) {
      return res.status(400).json({ error: 'logData is required' });
    }

    const parsed = await callInteractionScannerAgent(logData);

    const newInteraction = new Interaction({
      logText: logData,
      contactName: parsed.contact_name,
      role: parsed.role,
      interactionType: parsed.interaction_type,
      summary: parsed.summary,
      timestamp: parsed.timestamp
    });

    await newInteraction.save();

    res.json({ success: true, data: newInteraction });
  } catch (err) {
    console.error('Log upload error:', err);
    res.status(500).json({ error: 'Failed to process log' });
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
