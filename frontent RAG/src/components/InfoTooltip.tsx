import React from 'react'
import { FiInfo } from 'react-icons/fi'

interface InfoTooltipProps {
  info: string[]
}

export const InfoTooltip: React.FC<InfoTooltipProps> = ({ info }) => (
  <div className="relative inline-block group">
    <FiInfo className="text-blue-500 w-5 h-5 cursor-pointer" />
    <div
      className={
        `absolute bottom-full left-1/2 mb-2 transform -translate-x-1/2
        hidden group-hover:block
        bg-gray-800 text-white text-sm rounded-lg p-3
        whitespace-normal
        max-w-none w-max
        z-20`
      }
    >
      {info.length === 0 ? (
        <p className="mb-0">Brak danych</p>
      ) : (
        info.map((item, idx) => (
          <p key={idx} className="mb-1 last:mb-0">
            {item}
          </p>
        ))
      )}
    </div>
  </div>
)
