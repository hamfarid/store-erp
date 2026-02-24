/**
 * Standard Controller Template (v37.0)
 * Engine: Speckit v2.0
 */

const { validationResult } = require('express-validator');
const Service = require('../services/service');

exports.createItem = async (req, res, next) => {
  // 1. Sentinel Check: Input Validation
  const errors = validationResult(req);
  if (!errors.isEmpty()) {
    return res.status(400).json({ errors: errors.array() });
  }

  try {
    // 2. Business Logic
    const item = await Service.create(req.body);

    // 3. Response
    res.status(201).json({ data: item });
  } catch (error) {
    // 4. Error Handling (Centralized)
    next(error);
  }
};
