"use client";

import { useEffect, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";

type SplashScreenProps = {
  onDone: () => void;
  duration?: number;
};

export default function SplashScreen({ onDone, duration = 1800 }: SplashScreenProps) {
  const [visible, setVisible] = useState(true);

  useEffect(() => {
    const t = setTimeout(() => {
      setVisible(false);
      setTimeout(onDone, 400);
    }, duration);
    return () => clearTimeout(t);
  }, [duration, onDone]);

  return (
    <AnimatePresence>
      {visible && (
        <motion.div
          className="careloop-splash"
          initial={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 0.4 }}
        >
          <motion.div
            className="careloop-splash__content"
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ duration: 0.5, ease: "easeOut" }}
          >
            <div className="careloop-splash__icon">
              <svg width="48" height="48" viewBox="0 0 48 48" fill="none">
                <circle cx="24" cy="24" r="22" stroke="currentColor" strokeWidth="2" opacity="0.3" />
                <path
                  d="M16 24c0-4.4 3.6-8 8-8s8 3.6 8 8-3.6 8-8 8"
                  stroke="currentColor"
                  strokeWidth="2.5"
                  strokeLinecap="round"
                  className="careloop-splash__arc"
                />
                <circle cx="24" cy="24" r="3" fill="currentColor" />
              </svg>
            </div>
            <h1 className="careloop-splash__title">CareLoop</h1>
            <p className="careloop-splash__sub">
              Adaptive personality-aware caregiver assistant
            </p>
            <div className="careloop-splash__loader">
              <motion.div
                className="careloop-splash__loader-bar"
                initial={{ width: "0%" }}
                animate={{ width: "100%" }}
                transition={{ duration: duration / 1000, ease: "easeInOut" }}
              />
            </div>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
