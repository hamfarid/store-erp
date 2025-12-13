import React, { Suspense } from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { routes } from '../routes'
import LoadingSpinner from './common/LoadingSpinner'
import ErrorBoundary from './ErrorPages/ErrorBoundary'

const AppRouter = () => {
  return (
    <Router>
      <ErrorBoundary>
        <Suspense fallback={<LoadingSpinner />}>
          <Routes>
            {routes.map((route, index) => (
              <Route
                key={index}
                path={route.path}
                element={<route.element />}
              />
            ))}
            {/* Catch all route for 404 */}
            <Route path="*" element={<Navigate to="/error/404" replace />} />
          </Routes>
        </Suspense>
      </ErrorBoundary>
    </Router>
  )
}

export default AppRouter
