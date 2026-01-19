/**
 * Enhanced Footer Component
 * @file components/Layout/Footer.jsx
 */

import React from 'react';
import { Link } from 'react-router-dom';
import { cn } from '../../lib/utils';
import { 
  Heart, 
  Github, 
  Twitter, 
  Linkedin, 
  Mail,
  Sparkles,
  ExternalLink
} from 'lucide-react';

const Footer = ({ language = 'ar' }) => {
  const currentYear = new Date().getFullYear();

  const links = {
    main: [
      { label: 'لوحة التحكم', path: '/dashboard' },
      { label: 'المزارع', path: '/farms' },
      { label: 'التشخيص', path: '/diagnosis' },
      { label: 'التقارير', path: '/reports' },
    ],
    support: [
      { label: 'المساعدة', path: '/help' },
      { label: 'التوثيق', path: '/docs', external: true },
      { label: 'الدعم الفني', path: '/support' },
      { label: 'الأسئلة الشائعة', path: '/faq' },
    ],
    legal: [
      { label: 'سياسة الخصوصية', path: '/privacy' },
      { label: 'شروط الاستخدام', path: '/terms' },
    ],
  };

  const socialLinks = [
    { icon: Twitter, href: 'https://twitter.com/gaarascan', label: 'Twitter' },
    { icon: Github, href: 'https://github.com/gaarascan', label: 'GitHub' },
    { icon: Linkedin, href: 'https://linkedin.com/company/gaarascan', label: 'LinkedIn' },
    { icon: Mail, href: 'mailto:support@gaarascan.com', label: 'Email' },
  ];

  return (
    <footer className="bg-white dark:bg-gray-900 border-t border-gray-200 dark:border-gray-700">
      {/* Main Footer */}
      <div className="max-w-7xl mx-auto px-4 py-12">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {/* Brand Section */}
          <div className="lg:col-span-1">
            <div className="flex items-center gap-3 mb-4">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-emerald-500 to-teal-600 flex items-center justify-center shadow-lg">
                <Sparkles className="h-6 w-6 text-white" />
              </div>
              <div>
                <h3 className="font-bold text-gray-900 dark:text-gray-100">Gaara Scan AI</h3>
                <p className="text-xs text-gray-500 dark:text-gray-400">نظام الزراعة الذكية</p>
              </div>
            </div>
            <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">
              نظام متكامل للتشخيص الذكي للأمراض النباتية وإدارة المزارع باستخدام تقنيات الذكاء الاصطناعي المتقدمة.
            </p>
            {/* Social Links */}
            <div className="flex items-center gap-3">
              {socialLinks.map((social) => {
                const Icon = social.icon;
                return (
                  <a
                    key={social.label}
                    href={social.href}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="w-9 h-9 rounded-lg bg-gray-100 dark:bg-gray-800 flex items-center justify-center text-gray-600 dark:text-gray-400 hover:bg-emerald-100 hover:text-emerald-600 dark:hover:bg-emerald-900/30 dark:hover:text-emerald-400 transition-colors"
                    aria-label={social.label}
                  >
                    <Icon className="h-4 w-4" />
                  </a>
                );
              })}
            </div>
          </div>

          {/* Main Links */}
          <div>
            <h4 className="font-semibold text-gray-900 dark:text-gray-100 mb-4">الروابط الرئيسية</h4>
            <ul className="space-y-2">
              {links.main.map((link) => (
                <li key={link.path}>
                  <Link
                    to={link.path}
                    className="text-sm text-gray-600 dark:text-gray-400 hover:text-emerald-600 dark:hover:text-emerald-400 transition-colors"
                  >
                    {link.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Support Links */}
          <div>
            <h4 className="font-semibold text-gray-900 dark:text-gray-100 mb-4">الدعم والمساعدة</h4>
            <ul className="space-y-2">
              {links.support.map((link) => (
                <li key={link.path}>
                  {link.external ? (
                    <a
                      href={link.path}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-sm text-gray-600 dark:text-gray-400 hover:text-emerald-600 dark:hover:text-emerald-400 transition-colors inline-flex items-center gap-1"
                    >
                      {link.label}
                      <ExternalLink className="h-3 w-3" />
                    </a>
                  ) : (
                    <Link
                      to={link.path}
                      className="text-sm text-gray-600 dark:text-gray-400 hover:text-emerald-600 dark:hover:text-emerald-400 transition-colors"
                    >
                      {link.label}
                    </Link>
                  )}
                </li>
              ))}
            </ul>
          </div>

          {/* Newsletter / Contact */}
          <div>
            <h4 className="font-semibold text-gray-900 dark:text-gray-100 mb-4">تواصل معنا</h4>
            <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">
              اشترك للحصول على آخر التحديثات والميزات الجديدة.
            </p>
            <div className="flex gap-2">
              <input
                type="email"
                placeholder="بريدك الإلكتروني"
                className="flex-1 px-3 py-2 text-sm rounded-lg border border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800 focus:outline-none focus:ring-2 focus:ring-emerald-500"
              />
              <button className="px-4 py-2 bg-emerald-600 text-white text-sm font-medium rounded-lg hover:bg-emerald-700 transition-colors">
                اشتراك
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Bottom Bar */}
      <div className="border-t border-gray-100 dark:border-gray-800">
        <div className="max-w-7xl mx-auto px-4 py-4 flex flex-col md:flex-row items-center justify-between gap-4">
          <p className="text-sm text-gray-500 dark:text-gray-400 flex items-center gap-1">
            صُنع بـ <Heart className="h-4 w-4 text-red-500" /> في المملكة العربية السعودية © {currentYear}
          </p>
          <div className="flex items-center gap-4">
            {links.legal.map((link) => (
              <Link
                key={link.path}
                to={link.path}
                className="text-sm text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300 transition-colors"
              >
                {link.label}
              </Link>
            ))}
          </div>
          <p className="text-sm text-gray-500 dark:text-gray-400">
            الإصدار 4.3.0
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
