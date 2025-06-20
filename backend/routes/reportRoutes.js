import express from 'express';
import { generateStudentOKRReport } from '../controllers/generateReportController.js';

const router = express.Router();
router.post('/okr', generateStudentOKRReport);

export default router;
