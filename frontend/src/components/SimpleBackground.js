import React from 'react';
import { Box } from '@mui/material';

const SimpleBackground = () => {
  return (
    <Box
      sx={{
        position: 'fixed',
        top: 0,
        left: 0,
        width: '100%',
        height: '100%',
        zIndex: -1,
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        '&::before': {
          content: '""',
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          background: `
            radial-gradient(circle at 20% 80%, rgba(120, 119, 198, 0.3) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(255, 119, 198, 0.3) 0%, transparent 50%),
            radial-gradient(circle at 40% 40%, rgba(120, 219, 255, 0.2) 0%, transparent 50%)
          `,
          animation: 'float 6s ease-in-out infinite',
        },
        '&::after': {
          content: '""',
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          background: `
            repeating-linear-gradient(
              90deg,
              transparent,
              transparent 98px,
              rgba(255, 255, 255, 0.03) 100px
            ),
            repeating-linear-gradient(
              0deg,
              transparent,
              transparent 98px,
              rgba(255, 255, 255, 0.03) 100px
            )
          `,
        },
        '@keyframes float': {
          '0%, 100%': {
            transform: 'translateY(0px) rotate(0deg)',
          },
          '33%': {
            transform: 'translateY(-10px) rotate(1deg)',
          },
          '66%': {
            transform: 'translateY(5px) rotate(-1deg)',
          },
        },
      }}
    />
  );
};

export default SimpleBackground;
