import React from 'react';
import { Link } from 'react-router-dom';

const Error402 = () => {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-purple-900 via-indigo-800 to-blue-900">
      <div className="max-w-lg w-full mx-4 text-center">
        {/* Icon */}
        <div className="inline-flex items-center justify-center w-32 h-32 bg-purple-500 rounded-full mb-6 shadow-2xl">
          <span className="text-6xl">💳</span>
        </div>

        {/* Error Code */}
        <h1 className="text-8xl font-bold text-white mb-4 drop-shadow-lg">402</h1>

        {/* Title */}
        <h2 className="text-3xl font-bold text-white mb-4">الدفع مطلوب</h2>

        {/* Description */}
        <p className="text-purple-100 text-lg mb-8">
          هذه الميزة تتطلب اشتراكاً مدفوعاً.
          <br />
          يرجى ترقية حسابك للوصول إلى هذه الخدمة.
        </p>

        {/* Actions */}
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <Link
            to="/pricing"
            className="inline-flex items-center gap-2 bg-white hover:bg-purple-50 text-purple-900 font-bold py-3 px-8 rounded-xl transition shadow-lg"
          >
            <span>عرض الباقات</span>
            <span>💎</span>
          </Link>
          <Link
            to="/dashboard"
            className="inline-flex items-center gap-2 bg-transparent hover:bg-white/10 text-white font-bold py-3 px-8 rounded-xl transition border-2 border-white"
          >
            <span>لوحة التحكم</span>
            <span>📊</span>
          </Link>
        </div>

        {/* Error Details */}
        <div className="mt-12 p-4 bg-black/20 rounded-xl">
          <p className="text-purple-200 text-sm font-mono">
            HTTP 402 - Payment Required
          </p>
        </div>
      </div>
    </div>
  );
};

export default Error402;

