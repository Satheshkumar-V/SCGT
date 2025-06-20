import Interaction from '../models/Interaction.js';
import { callSocialCapitalReportAgent } from '../services/agentService.js';

export const generateStudentOKRReport = async (req, res) => {
  try {
    const { studentName } = req.body;
    if (!studentName) return res.status(400).json({ error: 'studentName is required' });

    const studentLogs = await Interaction.find({});

    const interactions = studentLogs.map(i => ({
      contact_name: i.contactName,
      summary: i.summary,
      quality_score: i.qualityScore,
      relevance_score: i.relevanceScore,
      reciprocity_status: i.reciprocityStatus
    }));

    const report = await callSocialCapitalReportAgent(interactions, studentName);

    res.json({ report });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Failed to generate OKR report' });
  }
};
