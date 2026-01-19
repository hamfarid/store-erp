import React from 'react';
import { Link } from 'react-router-dom';

const Error502 = () => {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-rose-900 via-pink-800 to-red-900">
      <div className="max-w-lg w-full mx-4 text-center">
        {/* Icon */}
        <div className="inline-flex items-center justify-center w-32 h-32 bg-rose-500 rounded-full mb-6 shadow-2xl animate-bounce">
          <span className="text-6xl">🌐</span>
        </div>

        {/* Error Code */}
        <h1 className="text-8xl font-bold text-white mb-4 drop-shadow-lg">502</h1>

        {/* Title */}
        <h2 className="text-3xl font-bold text-white mb-4">بوابة خاطئة</h2>

        {/* Description */}
        <p className="text-rose-100 text-lg mb-8">
          الخادم الوسيط تلقى استجابة غير صالحة من الخادم الرئيسي.
          <br />
          يرجى المحاولة مرة أخرى بعد قليل.
        </p>

        {/* Actions */}
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <button
            onClick={() => window.location.reload()}
            className="inline-flex items-center gap-2 bg-white hover:bg-rose-50 text-rose-900 font-bold py-3 px-8 rounded-xl transition shadow-lg"
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
          <p className="text-rose-200 text-sm font-mono">
            HTTP 502 - Bad Gateway
          </p>
        </div>
      </div>
    </div>
  );
};

export default Error502;

