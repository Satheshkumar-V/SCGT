import mongoose from 'mongoose';

const interactionSchema = new mongoose.Schema({
  logText: String,
  contactName: String,
  role: String,
  interactionType: String,
  summary: String,
  timestamp: String
}, { timestamps: true });

const Logs = mongoose.model('Interaction', interactionSchema);

export default Logs;
