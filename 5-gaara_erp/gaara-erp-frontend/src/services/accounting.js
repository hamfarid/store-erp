import api from "./api"

/**
 * Accounting Service
 * Handles all accounting and financial API calls
 */

// Chart of Accounts
export const getAccounts = async (params = {}) => {
  return api.get("/accounting/accounts", { params })
}

export const getAccountById = async (accountId) => {
  return api.get(`/accounting/accounts/${accountId}`)
}

export const createAccount = async (accountData) => {
  return api.post("/accounting/accounts", accountData)
}

export const updateAccount = async (accountId, accountData) => {
  return api.put(`/accounting/accounts/${accountId}`, accountData)
}

export const deleteAccount = async (accountId) => {
  return api.delete(`/accounting/accounts/${accountId}`)
}

// Journal Entries
export const getJournalEntries = async (params = {}) => {
  const { page = 1, limit = 20, dateFrom = "", dateTo = "", account = "" } = params
  const queryParams = new URLSearchParams({
    page: page.toString(),
    limit: limit.toString(),
    ...(dateFrom && { dateFrom }),
    ...(dateTo && { dateTo }),
    ...(account && { account }),
  })

  return api.get(`/accounting/journal-entries?${queryParams}`)
}

export const getJournalEntryById = async (entryId) => {
  return api.get(`/accounting/journal-entries/${entryId}`)
}

export const createJournalEntry = async (entryData) => {
  return api.post("/accounting/journal-entries", entryData)
}

export const updateJournalEntry = async (entryId, entryData) => {
  return api.put(`/accounting/journal-entries/${entryId}`, entryData)
}

export const deleteJournalEntry = async (entryId) => {
  return api.delete(`/accounting/journal-entries/${entryId}`)
}

export const approveJournalEntry = async (entryId) => {
  return api.post(`/accounting/journal-entries/${entryId}/approve`)
}

// Financial Reports
export const getBalanceSheet = async (params = {}) => {
  return api.get("/accounting/reports/balance-sheet", { params })
}

export const getIncomeStatement = async (params = {}) => {
  return api.get("/accounting/reports/income-statement", { params })
}

export const getCashFlow = async (params = {}) => {
  return api.get("/accounting/reports/cash-flow", { params })
}

export const getTrialBalance = async (params = {}) => {
  return api.get("/accounting/reports/trial-balance", { params })
}

export const getGeneralLedger = async (accountId, params = {}) => {
  return api.get(`/accounting/accounts/${accountId}/ledger`, { params })
}

// Transactions
export const getTransactions = async (params = {}) => {
  return api.get("/accounting/transactions", { params })
}

export const getTransactionById = async (transactionId) => {
  return api.get(`/accounting/transactions/${transactionId}`)
}

// Reconciliation
export const reconcileAccount = async (accountId, reconciliationData) => {
  return api.post(`/accounting/accounts/${accountId}/reconcile`, reconciliationData)
}

// Mock data for development
export const mockAccounts = [
  {
    id: 1,
    code: "1000",
    name: "الأصول",
    type: "asset",
    parentId: null,
    balance: 500000,
    children: [
      {
        id: 2,
        code: "1100",
        name: "الأصول المتداولة",
        type: "asset",
        parentId: 1,
        balance: 200000,
        children: [
          {
            id: 3,
            code: "1110",
            name: "النقدية",
            type: "asset",
            parentId: 2,
            balance: 150000,
            children: [],
          },
        ],
      },
    ],
  },
]

export default {
  getAccounts,
  getAccountById,
  createAccount,
  updateAccount,
  deleteAccount,
  getJournalEntries,
  getJournalEntryById,
  createJournalEntry,
  updateJournalEntry,
  deleteJournalEntry,
  approveJournalEntry,
  getBalanceSheet,
  getIncomeStatement,
  getCashFlow,
  getTrialBalance,
  getGeneralLedger,
  getTransactions,
  getTransactionById,
  reconcileAccount,
  mockAccounts,
}
