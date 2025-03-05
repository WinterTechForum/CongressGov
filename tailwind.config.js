module.exports = {
  content: [
    "./templates/**/*.html",
 ],
  theme: {
    extend: {
      dropShadow: {
        'md-intense': [
          '3px 4px 3px rgb(0 0 0 / 0.50)',
        ]
      }
    },
    screens: {
      xs: "360px",
      sm: "640px",
      md: "768px",
      lg: "1024px",
      xl: "1280px",
      "2xl": "1536px",
    },
  },
  plugins: [
    // require("@tailwindcss/forms"),
    // require("@tailwindcss/typography"),
    // require("@tailwindcss/aspect-ratio"),
  ],
};
