import React from 'react';
import { Link } from 'react-router-dom';

const Error504 = () => {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-sky-900 via-blue-800 to-indigo-900">
      <div className="max-w-lg w-full mx-4 text-center">
        {/* Icon */}
        <div className="inline-flex items-center justify-center w-32 h-32 bg-sky-500 rounded-full mb-6 shadow-2xl">
          <span className="text-6xl">⏱️</span>
        </div>

        {/* Error Code */}
        <h1 className="text-8xl font-bold text-white mb-4 drop-shadow-lg">504</h1>

        {/* Title */}
        <h2 className="text-3xl font-bold text-white mb-4">انتهت مهلة البوابة</h2>

        {/* Description */}
        <p className="text-sky-100 text-lg mb-8">
          الخادم استغرق وقتاً طويلاً للاستجابة.
          <br />
          قد يكون هناك بطء مؤقت في الشبكة. يرجى المحاولة مرة أخرى.
        </p>

        {/* Actions */}
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <button
            onClick={() => window.location.reload()}
            className="inline-flex items-center gap-2 bg-white hover:bg-sky-50 text-sky-900 font-bold py-3 px-8 rounded-xl transition shadow-lg"
          >
            <span>إعادة المحاولة</span>
            <span>🔄</span>
          </button>
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
          <p className="text-sky-200 text-sm font-mono">
            HTTP 504 - Gateway Timeout
          </p>
        </div>
      </div>
    </div>
  );
};

export default Error504;

