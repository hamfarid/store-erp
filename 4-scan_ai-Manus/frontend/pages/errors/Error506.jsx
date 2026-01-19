import React from 'react';
import { Link } from 'react-router-dom';

const Error506 = () => {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-emerald-900 via-teal-800 to-cyan-900">
      <div className="max-w-lg w-full mx-4 text-center">
        {/* Icon */}
        <div className="inline-flex items-center justify-center w-32 h-32 bg-emerald-500 rounded-full mb-6 shadow-2xl">
          <span className="text-6xl">🔀</span>
        </div>

        {/* Error Code */}
        <h1 className="text-8xl font-bold text-white mb-4 drop-shadow-lg">506</h1>

        {/* Title */}
        <h2 className="text-3xl font-bold text-white mb-4">تفاوض متغير أيضاً</h2>

        {/* Description */}
        <p className="text-emerald-100 text-lg mb-8">
          حدث خطأ في تكوين التفاوض على المحتوى.
          <br />
          يرجى التواصل مع الدعم الفني إذا استمرت المشكلة.
        </p>

        {/* Actions */}
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <Link
            to="/"
            className="inline-flex items-center gap-2 bg-white hover:bg-emerald-50 text-emerald-900 font-bold py-3 px-8 rounded-xl transition shadow-lg"
          >
            <span>الصفحة الرئيسية</span>
            <span>🏠</span>
          </Link>
          <button
            onClick={() => window.location.reload()}
            className="inline-flex items-center gap-2 bg-transparent hover:bg-white/10 text-white font-bold py-3 px-8 rounded-xl transition border-2 border-white"
          >
            <span>إعادة المحاولة</span>
            <span>🔄</span>
          </button>
        </div>

        {/* Error Details */}
        <div className="mt-12 p-4 bg-black/20 rounded-xl">
          <p className="text-emerald-200 text-sm font-mono">
            HTTP 506 - Variant Also Negotiates
          </p>
        </div>
      </div>
    </div>
  );
};

export default Error506;

