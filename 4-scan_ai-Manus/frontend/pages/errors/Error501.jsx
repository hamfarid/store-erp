import React from 'react';
import { Link } from 'react-router-dom';

const Error501 = () => {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-indigo-900 via-violet-800 to-purple-900">
      <div className="max-w-lg w-full mx-4 text-center">
        {/* Icon */}
        <div className="inline-flex items-center justify-center w-32 h-32 bg-indigo-500 rounded-full mb-6 shadow-2xl">
          <span className="text-6xl">🔧</span>
        </div>

        {/* Error Code */}
        <h1 className="text-8xl font-bold text-white mb-4 drop-shadow-lg">501</h1>

        {/* Title */}
        <h2 className="text-3xl font-bold text-white mb-4">غير مُنفَّذ</h2>

        {/* Description */}
        <p className="text-indigo-100 text-lg mb-8">
          هذه الميزة غير مدعومة حالياً أو لم يتم تنفيذها بعد.
          <br />
          سنضيفها في التحديثات القادمة.
        </p>

        {/* Actions */}
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <Link
            to="/dashboard"
            className="inline-flex items-center gap-2 bg-white hover:bg-indigo-50 text-indigo-900 font-bold py-3 px-8 rounded-xl transition shadow-lg"
          >
            <span>لوحة التحكم</span>
            <span>📊</span>
          </Link>
          <Link
            to="/"
            className="inline-flex items-center gap-2 bg-transparent hover:bg-white/10 text-white font-bold py-3 px-8 rounded-xl transition border-2 border-white"
          >
            <span>الصفحة الرئيسية</span>
            <span>🏠</span>
          </Link>
        </div>

        {/* Error Details */}
        <div className="mt-12 p-4 bg-black/20 rounded-xl">
          <p className="text-indigo-200 text-sm font-mono">
            HTTP 501 - Not Implemented
          </p>
        </div>
      </div>
    </div>
  );
};

export default Error501;

