const PREC = {
  COMMENT: 1,
};

module.exports = grammar({
  name: 'imgoatex',

  extras: $ => [
    /\s/,
  ],

  rules: {
    source_file: $ => repeat($._statement),

    _statement: $ => choice(
      $.meta,
      $.section,
      $.subsection,
      $.begin_frame,
      $.end_frame,
      $.video,
      $.image,
      $.textbox,
      $.item,
      $.subitem,
      $.pause,
      $.comment,
      $.text
    ),

    meta: $ => token(seq('%', /[^\n]+/, ':', /\s*/, /[^\n]+/)),

    section: $ => token(seq('\\section{', /[^}]+/, '}')),

    subsection: $ => token(seq('\\subsection{', /[^}]+/, '}')),

    begin_frame: $ => seq(
      '\\begin{frame}',
      optional(seq('{', /[^}]*/, '}')),
      optional(seq('{', /[^}]*/, '}')),
      optional(seq('[', /[^\]]*/, ']'))
    ),

    end_frame: $ => token('\\end{frame}'),

    video: $ => seq(
      '\\video{', /[^}]+/, '}',
      optional(seq('[', /[^\]]*/, ']'))
    ),

    image: $ => seq(
      '\\image{', /[^}]+/, '}',
      optional(seq('[', /[^\]]*/, ']'))
    ),

    textbox: $ => seq(
      '\\textbox{', repeat(choice(/\$[^$]*\$/, /[^}]/)), '}',
      optional(seq('[', /[^\]]*/, ']'))
    ),

    item: $ => seq('\\item{', repeat(choice(/\$[^$]*\$/, /[^}]/)), '}'),

    subitem: $ => seq('\\subitem{', repeat(choice(/\$[^$]*\$/, /[^}]/)), '}'),

    pause: $ => token('\\pause'),

    comment: $ => token(seq('#', /.*/)),

    text: $ => token(/[^\\#%\n]+/),
  }
});
