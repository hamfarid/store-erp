import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

const Error503 = () => {
  const [countdown, setCountdown] = useState(30);

  useEffect(() => {
    const timer = setInterval(() => {
      setCountdown(prev => {
        if (prev <= 1) {
          window.location.reload();
          return 30;
        }
        return prev - 1;
      });
    }, 1000);

    return () => clearInterval(timer);
  }, []);

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-amber-900 via-orange-800 to-yellow-900">
      <div className="max-w-lg w-full mx-4 text-center">
        {/* Icon */}
        <div className="inline-flex items-center justify-center w-32 h-32 bg-amber-500 rounded-full mb-6 shadow-2xl">
          <span className="text-6xl">🛠️</span>
        </div>

        {/* Error Code */}
        <h1 className="text-8xl font-bold text-white mb-4 drop-shadow-lg">503</h1>

        {/* Title */}
        <h2 className="text-3xl font-bold text-white mb-4">الخدمة غير متاحة</h2>

        {/* Description */}
        <p className="text-amber-100 text-lg mb-8">
          الخادم تحت الصيانة أو مُحمَّل بشكل زائد حالياً.
          <br />
          سيتم إعادة المحاولة تلقائياً خلال {countdown} ثانية.
        </p>

        {/* Countdown Bar */}
        <div className="w-full bg-black/20 rounded-full h-2 mb-8">
          <div 
            className="bg-white h-2 rounded-full transition-all duration-1000"
            style={{ width: `${(countdown / 30) * 100}%` }}
          ></div>
        </div>

        {/* Actions */}
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <button
            onClick={() => window.location.reload()}
            className="inline-flex items-center gap-2 bg-white hover:bg-amber-50 text-amber-900 font-bold py-3 px-8 rounded-xl transition shadow-lg"
          >
            <span>إعادة المحاولة الآن</span>
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
          <p className="text-amber-200 text-sm font-mono">
            HTTP 503 - Service Unavailable
          </p>
          <p className="text-amber-300 text-xs mt-2">
            نعمل على إعادة الخدمة في أقرب وقت ممكن
          </p>
        </div>
      </div>
    </div>
  );
};

export default Error503;

