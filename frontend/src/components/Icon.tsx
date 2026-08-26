interface IconProps {
  name:
    | 'briefcase'
    | 'copy'
    | 'download'
    | 'file'
    | 'mail'
    | 'phone'
    | 'thumbs-down'
    | 'thumbs-up'
    | 'user'
  size?: number
}

export function Icon({ name, size = 22 }: IconProps) {
  const commonProps = {
    width: size,
    height: size,
    viewBox: '0 0 24 24',
    fill: 'none',
    stroke: 'currentColor',
    strokeWidth: 1.8,
    strokeLinecap: 'round' as const,
    strokeLinejoin: 'round' as const,
    'aria-hidden': true,
  }

  switch (name) {
    case 'briefcase':
      return (
        <svg {...commonProps}>
          <rect x="3" y="7" width="18" height="13" rx="2" />
          <path d="M8 7V5.5A1.5 1.5 0 0 1 9.5 4h5A1.5 1.5 0 0 1 16 5.5V7M3 12h18M10 12v2h4v-2" />
        </svg>
      )
    case 'copy':
      return (
        <svg {...commonProps}>
          <rect x="9" y="9" width="10" height="10" rx="2" />
          <path d="M15 9V7a2 2 0 0 0-2-2H7a2 2 0 0 0-2 2v6a2 2 0 0 0 2 2h2" />
        </svg>
      )
    case 'download':
      return (
        <svg {...commonProps}>
          <path d="M12 3v12m0 0 4-4m-4 4-4-4M5 20h14" />
        </svg>
      )
    case 'file':
      return (
        <svg {...commonProps}>
          <path d="M6 3h8l4 4v14H6z" />
          <path d="M14 3v5h5M9 13h6M9 17h6" />
        </svg>
      )
    case 'mail':
      return (
        <svg {...commonProps}>
          <rect x="3" y="5" width="18" height="14" rx="2" />
          <path d="m4 7 8 6 8-6" />
        </svg>
      )
    case 'phone':
      return (
        <svg {...commonProps}>
          <path d="M7.2 3.5 4.8 5.9c-.8.8-.2 3.2 1.4 5.7s3.7 4.6 6.2 6.2 4.9 2.2 5.7 1.4l2.4-2.4-4.2-3.1-2.1 2.1c-1.6-.8-2.8-1.7-4-2.9-1.2-1.2-2.1-2.4-2.9-4l2.1-2.1z" />
        </svg>
      )
    case 'thumbs-down':
      return (
        <svg {...commonProps}>
          <path d="M17 14V2" />
          <path d="M9 18.1 10 14H4.2a2 2 0 0 1-1.9-2.6l2.3-8A2 2 0 0 1 6.5 2H20a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2h-2.8a2 2 0 0 0-1.8 1.1L12 22a3.1 3.1 0 0 1-3-3.9Z" />
        </svg>
      )
    case 'thumbs-up':
      return (
        <svg {...commonProps}>
          <path d="M7 10v12" />
          <path d="m15 5.9-1 4.1h5.8a2 2 0 0 1 1.9 2.6l-2.3 8A2 2 0 0 1 17.5 22H4a2 2 0 0 1-2-2v-8a2 2 0 0 1 2-2h2.8a2 2 0 0 0 1.8-1.1L12 2a3.1 3.1 0 0 1 3 3.9Z" />
        </svg>
      )
    case 'user':
      return (
        <svg {...commonProps}>
          <circle cx="12" cy="8" r="4" />
          <path d="M4 21v-2a6 6 0 0 1 6-6h4a6 6 0 0 1 6 6v2z" />
        </svg>
      )
  }
}
