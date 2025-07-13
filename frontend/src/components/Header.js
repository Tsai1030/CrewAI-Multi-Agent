import React from 'react';
import { AppBar, Toolbar, Typography, Box } from '@mui/material';
import { styled } from '@mui/material/styles';
import { motion } from 'framer-motion';

const StyledAppBar = styled(AppBar)(({ theme }) => ({
  background: 'rgba(255, 255, 255, 0.1)',
  backdropFilter: 'blur(15px)',
  border: 'none',
  boxShadow: '0 2px 20px rgba(0, 0, 0, 0.1)',
  height: '64px', // 明確設置 Header 高度
  '& .MuiToolbar-root': {
    minHeight: '64px',
    [theme.breakpoints.down('sm')]: {
      minHeight: '56px',
    },
  },
}));

const Header = () => {
  return (
    <StyledAppBar position="fixed" elevation={0}>
      <Toolbar>
        <motion.div
          initial={{ opacity: 0, x: -50 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.6 }}
          style={{ display: 'flex', alignItems: 'center', flexGrow: 1 }}
        >
          <Typography
            variant="h6"
            component="div"
            sx={{
              fontFamily: '"Cinzel", serif',
              fontWeight: 600,
              background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
              fontSize: { xs: '1rem', sm: '1.25rem', md: '1.5rem' },
              whiteSpace: 'nowrap',
              overflow: 'hidden',
              textOverflow: 'ellipsis',
            }}
          >
            🌟 紫微斗數 AI 系統
          </Typography>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, x: 50 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
        >
          <Box sx={{ display: { xs: 'none', sm: 'flex' }, alignItems: 'center', gap: 1 }}>
            <Typography
              variant="body2"
              color="text.secondary"
              sx={{
                fontSize: { sm: '0.8rem', md: '0.875rem' },
                whiteSpace: 'nowrap'
              }}
            >
              智能命理分析平台
            </Typography>
          </Box>
        </motion.div>
      </Toolbar>
    </StyledAppBar>
  );
};

export default Header;
