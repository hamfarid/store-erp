import React from 'react'

const ThemeColors = {
  primary: '#80AA45',
  secondary: '#3B715A',
  accent: '#E65E36',
  danger: '#C7451F',
  success: '#80AA45',
  warning: '#E65E36',
  info: '#3B715A',
  white: '#ffffff',
  gray: '#6b7280',
}

export const ThemedIcon = ({ 
  icon: Icon, 
  variant = 'primary', 
  size = 20, 
  className = '',
  ...props 
}) => {
  const color = ThemeColors[variant] || variant
  return (
    <Icon 
      color={color} 
      size={size} 
      className={className}
      {...props}
    />
  )
}

// Icon variants by use case
export const IconVariants = {
  navigation: { variant: 'primary', size: 20 },
  action: { variant: 'primary', size: 18 },
  status_success: { variant: 'success', size: 16 },
  status_error: { variant: 'danger', size: 16 },
  status_warning: { variant: 'warning', size: 16 },
  header: { variant: 'primary', size: 24 },
  sidebar: { variant: 'gray', size: 20 },
  sidebar_active: { variant: 'primary', size: 20 },
  button_primary: { variant: 'white', size: 16 },
  button_secondary: { variant: 'primary', size: 16 },
}

export default ThemedIcon
