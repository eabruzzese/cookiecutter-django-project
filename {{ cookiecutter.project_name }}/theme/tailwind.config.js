const { DISABLE_PURGE = false } = process.env;

module.exports = {
  content: [
    // Scan Django templates and javascript files for Tailwind class names.
    "../{{ cookiecutter.package_name }}/**/templates/**/*.html",
    "../{{ cookiecutter.package_name }}/**/static/**/*.js",
  ],
  safelist: DISABLE_PURGE ? [{ pattern: /.*/ }] : [],
  theme: {
    extend: {}
  },
  plugins: [
    require('@tailwindcss/typography'),
    require('@tailwindcss/forms'),
    require('@tailwindcss/line-clamp'),
    require('@tailwindcss/aspect-ratio'),
  ]
}
