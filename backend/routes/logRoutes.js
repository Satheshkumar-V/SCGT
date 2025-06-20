import express from 'express';
import { handleLogUpload, getAllInteractions } from '../controllers/logController.js';
const router = express.Router();

router.post('/upload', handleLogUpload);
router.get('/all', getAllInteractions);

export default router;
