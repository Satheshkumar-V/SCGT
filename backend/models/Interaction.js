import mongoose from 'mongoose';

const interactionSchema = new mongoose.Schema({
  logText: String,
  contactName: String,
  role: String,
  interactionType: String,
  summary: String,
  timestamp: String,

  // Agent 2
  qualityScore: Number,
  qualityBreakdown: Object,
  qualityExplanation: String,

  // Agent 3
  relevanceScore: Number,
  contactAlignment: Boolean,
  contentRelevance: Boolean,
  goalMatchReasoning: String,

  reciprocityStatus: String,
  reciprocityEvidence: String
}, { timestamps: true });



const Interaction = mongoose.model('Interaction', interactionSchema);

export default Interaction;
