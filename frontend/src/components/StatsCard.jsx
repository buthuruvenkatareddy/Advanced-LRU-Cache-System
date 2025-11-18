import clsx from 'clsx';

function StatsCard({ title, value, icon: Icon, iconColor, subtitle, trend }) {
  return (
    <div className="stat-card">
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <p className="text-sm font-medium text-gray-600 mb-1">{title}</p>
          <h3 className="text-3xl font-bold text-gray-900">{value}</h3>
          {subtitle && (
            <p className="text-xs text-gray-500 mt-1">{subtitle}</p>
          )}
          {trend && (
            <p className={clsx(
              'text-xs mt-2 font-medium',
              trend.direction === 'up' ? 'text-green-600' : 'text-red-600'
            )}>
              {trend.value}
            </p>
          )}
        </div>
        <div className={clsx(
          'p-3 rounded-lg',
          iconColor || 'bg-primary-100'
        )}>
          <Icon className={clsx(
            'w-6 h-6',
            iconColor ? '' : 'text-primary-600'
          )} />
        </div>
      </div>
    </div>
  );
}

export default StatsCard;
