'use client';

import * as motion from 'motion/react-client';
import { useState } from 'react';

export default function LayoutAnimation() {
  const [isOn, setIsOn] = useState(false);

  const toggleSwitch = () => setIsOn(!isOn);

  return (
    <div className="flex flex-col items-center justify-center gap-4">
      <motion.button
        className="toggle-container"
        style={{
          ...container,
          backgroundColor: isOn ? 'var(--hue-6)' : 'var(--hue-3-transparent)',
          justifyContent: isOn ? 'flex-end' : 'flex-start',
        }}
        onClick={toggleSwitch}
        animate={{
          scale: isOn ? 1.05 : 1,
        }}
        whileHover={{
          scale: isOn ? 1.1 : 1.05,
          boxShadow: isOn
            ? '0 0 15px 2px var(--hue-6)'
            : '0 0 10px 1px var(--hue-3-transparent)',
        }}
        transition={{
          duration: 0.2,
        }}
      >
        <motion.div
          className="toggle-handle"
          style={{
            ...handle,
            backgroundColor: isOn ? 'var(--white)' : 'var(--hue-3)',
          }}
          layout
          transition={{
            type: 'spring',
            stiffness: 700,
            damping: 30,
          }}
          animate={{
            rotate: isOn ? 180 : 0,
          }}
        >
          {isOn && (
            <motion.div
              initial={{ opacity: 0, scale: 0 }}
              animate={{ opacity: 1, scale: 1 }}
              className="flex items-center justify-center h-full"
            ></motion.div>
          )}
        </motion.div>
      </motion.button>
    </div>
  );
}

/**
 * ==============   Styles   ================
 */

const container = {
  width: 100,
  height: 50,
  borderRadius: 50,
  cursor: 'pointer',
  display: 'flex',
  padding: 10,
  transition: 'background-color 0.3s ease',
};

const handle = {
  width: 50,
  height: 50,
  borderRadius: '50%',
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
};
