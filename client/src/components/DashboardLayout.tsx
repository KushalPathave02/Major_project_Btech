import React, { useEffect, useMemo, useState } from 'react';
import { Box, Drawer, AppBar, Toolbar, Typography, List, ListItem, ListItemIcon, ListItemText, CssBaseline, Avatar, InputBase, IconButton, ThemeProvider, createTheme, Badge, Menu, ToggleButtonGroup, ToggleButton, Button, Dialog, DialogActions, DialogContent, DialogContentText, DialogTitle } from '@mui/material';
import DashboardIcon from '@mui/icons-material/Dashboard';
import UploadFileIcon from '@mui/icons-material/UploadFile';
import AccountBalanceWalletIcon from '@mui/icons-material/AccountBalanceWallet';
import BarChartIcon from '@mui/icons-material/BarChart';
import PersonIcon from '@mui/icons-material/Person';
import SettingsIcon from '@mui/icons-material/Settings';
import LogoutIcon from '@mui/icons-material/Logout';
import NotificationsIcon from '@mui/icons-material/Notifications';
import SearchIcon from '@mui/icons-material/Search';
import { useNavigate } from 'react-router-dom';

const drawerWidth = 220;

const navItems = [
  { text: 'Dashboard', icon: <DashboardIcon />, path: '/dashboard' },
  { text: 'Transactions', icon: <UploadFileIcon />, path: '/upload' },
  { text: 'Wallet', icon: <AccountBalanceWalletIcon />, path: '/wallet' },
  { text: 'Analytics', icon: <BarChartIcon />, path: '/analytics' },
  { text: 'Personal', icon: <PersonIcon />, path: '/personal' },

];

import { useTheme } from '../ThemeContext';
import { useCurrency } from '../CurrencyContext';

const DashboardLayout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const navigate = useNavigate();
  const [profileAnchorEl, setProfileAnchorEl] = useState<null | HTMLElement>(null);
  const [profile, setProfile] = useState<{ name?: string; email?: string; profilePic?: string; role?: string } | null>(null);
  const [profileLoading, setProfileLoading] = useState(false);
  const [avatarSrc, setAvatarSrc] = useState<string | undefined>(undefined);
  const [openLogoutDialog, setOpenLogoutDialog] = useState(false);

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/login');
  };

  const handleOpenLogoutDialog = () => {
    setOpenLogoutDialog(true);
  };

  const handleCloseLogoutDialog = () => {
    setOpenLogoutDialog(false);
  };
  const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';
  const { currency, setCurrency } = useCurrency();
  const { theme, toggleTheme } = useTheme();

  React.useEffect(() => {
    if (profileAnchorEl) {
      setProfileLoading(true);
      const token = localStorage.getItem('token');
      const API_URL = process.env.REACT_APP_API_URL;
fetch(`${API_URL}/users/profile`, {
        headers: {
          Authorization: token ? `Bearer ${token}` : '',
        },
      })
        .then(res => res.json())
        .then(data => {
          if (data && (data.name || data.email)) {
            setProfile({ name: data.name, email: data.email, role: data.role, profilePic: data.profilePic });
          } else {
            setProfile({
              name: localStorage.getItem('name') || 'Candidate',
              email: localStorage.getItem('email') || 'example@email.com',
              role: localStorage.getItem('role') || 'analyst',
              profilePic: localStorage.getItem('profilePic') || undefined
            });
          }
        })
        .catch(() => {
          setProfile({
            name: localStorage.getItem('name') || 'Candidate',
            email: localStorage.getItem('email') || 'example@email.com',
            role: localStorage.getItem('role') || 'analyst',
            profilePic: localStorage.getItem('profilePic') || undefined
          });
        })
        .finally(() => setProfileLoading(false));
    }
  }, [profileAnchorEl]);

  // Compute avatar src whenever profile or localStorage changes
  useEffect(() => {
    const computeSrc = () => {
      const pic = profile?.profilePic || localStorage.getItem('profilePic') || undefined;
      if (!pic) return setAvatarSrc(undefined);
      if (pic.startsWith('http')) return setAvatarSrc(pic);
      return setAvatarSrc(`${API_URL}${pic}`);
    };
    computeSrc();
  }, [profile, API_URL]);

  // Listen for storage changes and custom event from Personal page
  useEffect(() => {
    const onStorage = (e: StorageEvent) => {
      if (e.key === 'profilePic') {
        const val = e.newValue || undefined;
        if (!val) setAvatarSrc(undefined);
        else setAvatarSrc(val.startsWith('http') ? val : `${API_URL}${val}`);
      }
    };
    const onCustom = () => {
      const val = localStorage.getItem('profilePic') || undefined;
      if (!val) setAvatarSrc(undefined);
      else setAvatarSrc(val.startsWith('http') ? val : `${API_URL}${val}`);
    };
    window.addEventListener('storage', onStorage);
    window.addEventListener('profilePicUpdated', onCustom as any);
    return () => {
      window.removeEventListener('storage', onStorage);
      window.removeEventListener('profilePicUpdated', onCustom as any);
    };
  }, [API_URL]);

  return (
    <>
      <CssBaseline />
      <Box sx={{ display: 'flex', minHeight: '100vh', background: (theme) => theme.palette.background.default }}>
        {/* Sidebar */}
        <Drawer
          variant="permanent"
          sx={{
            width: drawerWidth,
            flexShrink: 0,
            [`& .MuiDrawer-paper`]: {
              width: drawerWidth,
              boxSizing: 'border-box',
              background: theme === 'dark' 
                ? 'linear-gradient(180deg, #181c2a 0%, #23263a 100%)' 
                : 'linear-gradient(180deg, #ffffff 0%, #f8f9fc 100%)',
              color: theme === 'dark' ? '#fff' : '#23263a',
              borderRight: theme === 'dark' ? '1px solid #23263a' : '1px solid #e0e4eb',
            },
          }}
        >
          <Toolbar sx={{ minHeight: 80 }}>
            <Typography variant="h6" noWrap component="div" sx={{ fontWeight: 700, letterSpacing: 1 }}>
              FinTrack+
            </Typography>
          </Toolbar>
          <List>
            {navItems.map((item) => (
              <ListItem button key={item.text} onClick={() => navigate(item.path)}>
                <ListItemIcon sx={{ color: theme === 'dark' ? '#b0b8d1' : '#5d5d7c' }}>{item.icon}</ListItemIcon>
                <ListItemText primary={item.text} />
              </ListItem>
            ))}
            <ListItem button onClick={handleOpenLogoutDialog}>
              <ListItemIcon sx={{ color: theme === 'dark' ? '#b0b8d1' : '#5d5d7c' }}><LogoutIcon /></ListItemIcon>
              <ListItemText primary="Logout" />
            </ListItem>
          </List>
        </Drawer>

        {/* Logout Confirmation Dialog */}
        <Dialog
          open={openLogoutDialog}
          onClose={handleCloseLogoutDialog}
          aria-labelledby="alert-dialog-title"
          aria-describedby="alert-dialog-description"
          PaperProps={{
            style: {
              background: theme === 'dark' ? '#23263a' : '#ffffff',
              color: theme === 'dark' ? '#ffffff' : '#23263a',
              borderRadius: '12px',
              padding: '20px',
              boxShadow: '0 8px 32px rgba(0, 0, 0, 0.1)'
            }
          }}
        >
          <DialogTitle id="alert-dialog-title" style={{ fontWeight: 600, fontSize: '1.2rem' }}>
            Confirm Logout
          </DialogTitle>
          <DialogContent>
            <DialogContentText id="alert-dialog-description" style={{ color: theme === 'dark' ? '#b0b8d1' : '#5d5d7c' }}>
              Are you sure you want to logout?
            </DialogContentText>
          </DialogContent>
          <DialogActions style={{ padding: '16px 24px' }}>
            <Button 
              onClick={handleCloseLogoutDialog} 
              style={{
                color: theme === 'dark' ? '#b0b8d1' : '#5d5d7c',
                textTransform: 'none',
                fontWeight: 500
              }}
            >
              Cancel
            </Button>
            <Button 
              onClick={handleLogout} 
              autoFocus
              style={{
                background: 'linear-gradient(120deg, #7c3aed 0%, #7c3aed 100%)',
                color: 'white',
                textTransform: 'none',
                fontWeight: 600,
                padding: '6px 16px',
                borderRadius: '8px',
                boxShadow: 'none'
              }}
            >
              Logout
            </Button>
          </DialogActions>
        </Dialog>

        {/* Main content */}
        <Box component="main" sx={{ flexGrow: 1, p: 0, ml: `${drawerWidth}px`, background: (theme) => theme.palette.background.default, minHeight: '100vh' }}>
          <AppBar
            position="fixed"
            sx={{ 
              width: `calc(100% - ${drawerWidth}px)`, 
              ml: `${drawerWidth}px`, 
              background: theme === 'dark' ? '#23263a' : '#ffffff', 
              color: theme === 'dark' ? '#fff' : '#23263a', 
              boxShadow: 'none', 
              borderBottom: theme === 'dark' ? '1px solid #23263a' : '1px solid #e0e4eb' 
            }}
          >
            <Toolbar sx={{ minHeight: 80, display: 'flex', justifyContent: 'flex-end' }}>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                {/* Theme Toggle */}
                <Button
                  onClick={toggleTheme}
                  variant="outlined"
                  size="small"
                  sx={{ 
                    mr: 1, 
                    color: theme === 'dark' ? '#b0b8d1' : '#23263a',
                    borderColor: theme === 'dark' ? '#b0b8d1' : '#23263a',
                    '&:hover': {
                      borderColor: theme === 'dark' ? '#fff' : '#7c3aed',
                      color: theme === 'dark' ? '#fff' : '#7c3aed'
                    }
                  }}
                >
                  {theme === 'dark' ? '☀️' : '🌙'}
                </Button>

                {/* Currency Switcher */}
                <ToggleButtonGroup
                  exclusive
                  color="secondary"
                  size="small"
                  value={currency}
                  onChange={(_, val) => { if (val) setCurrency(val); }}
                  sx={{ 
                    mr: 1, 
                    background: theme === 'dark' ? '#1c2030' : '#f0f0f5', 
                    borderRadius: 2 
                  }}
                >
                  <ToggleButton value="INR" sx={{ color: theme === 'dark' ? '#b0b8d1' : '#23263a' }}>INR</ToggleButton>
                  <ToggleButton value="USD" sx={{ color: theme === 'dark' ? '#b0b8d1' : '#23263a' }}>USD</ToggleButton>
                  <ToggleButton value="EUR" sx={{ color: theme === 'dark' ? '#b0b8d1' : '#23263a' }}>EUR</ToggleButton>
                </ToggleButtonGroup>

              </Box>
            </Toolbar>
          </AppBar>
          <Toolbar sx={{ minHeight: 80 }} /> {/* Spacer for AppBar */}
          <Box sx={{ p: 2, pl: 2, pr: 0, ml: -20,mr:12 }}>{children}</Box>
        </Box>
      </Box>
    </> 
  );
};

export default DashboardLayout;
