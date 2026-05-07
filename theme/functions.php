<?php
/**
 * Astra functions and definitions
 *
 * @link https://developer.wordpress.org/themes/basics/theme-functions/
 *
 * @package Astra
 * @since 1.0.0
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit; // Exit if accessed directly.
}

/**
 * Define Constants
 */
define( 'ASTRA_THEME_VERSION', '4.13.0' );
define( 'ASTRA_THEME_SETTINGS', 'astra-settings' );
define( 'ASTRA_THEME_DIR', trailingslashit( get_template_directory() ) );
define( 'ASTRA_THEME_URI', trailingslashit( esc_url( get_template_directory_uri() ) ) );
define( 'ASTRA_THEME_ORG_VERSION', file_exists( ASTRA_THEME_DIR . 'inc/w-org-version.php' ) );

define( 'ASTRA_EXT_MIN_VER', '4.12.0' );

if ( ASTRA_THEME_ORG_VERSION ) {
	require_once ASTRA_THEME_DIR . 'inc/w-org-version.php';
}

require_once ASTRA_THEME_DIR . 'inc/core/class-astra-theme-options.php';
require_once ASTRA_THEME_DIR . 'inc/core/class-theme-strings.php';
require_once ASTRA_THEME_DIR . 'inc/core/common-functions.php';
require_once ASTRA_THEME_DIR . 'inc/core/class-astra-icons.php';

define( 'ASTRA_WEBSITE_BASE_URL', 'https://wpastra.com' );

require_once ASTRA_THEME_DIR . 'inc/theme-update/astra-update-functions.php';
require_once ASTRA_THEME_DIR . 'inc/theme-update/class-astra-theme-background-updater.php';

require_once ASTRA_THEME_DIR . 'inc/customizer/class-astra-font-families.php';
if ( is_admin() ) {
	require_once ASTRA_THEME_DIR . 'inc/customizer/class-astra-fonts-data.php';
}

require_once ASTRA_THEME_DIR . 'inc/lib/webfont/class-astra-webfont-loader.php';
require_once ASTRA_THEME_DIR . 'inc/lib/docs/class-astra-docs-loader.php';
require_once ASTRA_THEME_DIR . 'inc/customizer/class-astra-fonts.php';

require_once ASTRA_THEME_DIR . 'inc/dynamic-css/custom-menu-old-header.php';
require_once ASTRA_THEME_DIR . 'inc/dynamic-css/container-layouts.php';
require_once ASTRA_THEME_DIR . 'inc/dynamic-css/astra-icons.php';
require_once ASTRA_THEME_DIR . 'inc/core/class-astra-walker-page.php';
require_once ASTRA_THEME_DIR . 'inc/core/class-astra-enqueue-scripts.php';
require_once ASTRA_THEME_DIR . 'inc/core/class-gutenberg-editor-css.php';
require_once ASTRA_THEME_DIR . 'inc/core/class-astra-wp-editor-css.php';
require_once ASTRA_THEME_DIR . 'inc/core/class-astra-command-palette.php';
require_once ASTRA_THEME_DIR . 'inc/dynamic-css/block-editor-compatibility.php';
require_once ASTRA_THEME_DIR . 'inc/dynamic-css/inline-on-mobile.php';
require_once ASTRA_THEME_DIR . 'inc/dynamic-css/content-background.php';
require_once ASTRA_THEME_DIR . 'inc/dynamic-css/dark-mode.php';
require_once ASTRA_THEME_DIR . 'inc/class-astra-dynamic-css.php';
require_once ASTRA_THEME_DIR . 'inc/class-astra-global-palette.php';

if ( ! defined( 'ASTRA_SITES_VER' ) || version_compare( ASTRA_SITES_VER, '4.3.7', '<' ) || version_compare( ASTRA_SITES_VER, '4.4.4', '>' ) ) {
	require_once ASTRA_THEME_DIR . 'inc/lib/class-astra-nps-notice.php';
	require_once ASTRA_THEME_DIR . 'inc/lib/class-astra-nps-survey.php';
}

require_once ASTRA_THEME_DIR . 'inc/core/class-astra-attr.php';
require_once ASTRA_THEME_DIR . 'inc/template-tags.php';

require_once ASTRA_THEME_DIR . 'inc/widgets.php';
require_once ASTRA_THEME_DIR . 'inc/core/theme-hooks.php';
require_once ASTRA_THEME_DIR . 'inc/admin-functions.php';
require_once ASTRA_THEME_DIR . 'inc/class-astra-memory-limit-notice.php';
require_once ASTRA_THEME_DIR . 'inc/core/sidebar-manager.php';

require_once ASTRA_THEME_DIR . 'inc/markup-extras.php';
require_once ASTRA_THEME_DIR . 'inc/extras.php';
require_once ASTRA_THEME_DIR . 'inc/blog/blog-config.php';
require_once ASTRA_THEME_DIR . 'inc/blog/blog.php';
require_once ASTRA_THEME_DIR . 'inc/blog/single-blog.php';

require_once ASTRA_THEME_DIR . 'inc/template-parts.php';
require_once ASTRA_THEME_DIR . 'inc/class-astra-loop.php';
require_once ASTRA_THEME_DIR . 'inc/class-astra-mobile-header.php';

require_once ASTRA_THEME_DIR . 'inc/class-astra-after-setup-theme.php';

require_once ASTRA_THEME_DIR . 'inc/core/class-astra-admin-helper.php';

require_once ASTRA_THEME_DIR . 'inc/schema/class-astra-schema.php';

require_once ASTRA_THEME_DIR . 'admin/includes/class-astra-learn.php';
require_once ASTRA_THEME_DIR . 'admin/includes/class-astra-api-init.php';

if ( is_admin() ) {
	require_once ASTRA_THEME_DIR . 'inc/core/class-astra-admin-settings.php';
	require_once ASTRA_THEME_DIR . 'admin/class-astra-admin-loader.php';
	require_once ASTRA_THEME_DIR . 'inc/lib/astra-notices/class-bsf-admin-notices.php';
}

require_once ASTRA_THEME_DIR . 'admin/class-astra-bsf-analytics.php';

require_once ASTRA_THEME_DIR . 'inc/metabox/class-astra-meta-boxes.php';
require_once ASTRA_THEME_DIR . 'inc/metabox/class-astra-meta-box-operations.php';
require_once ASTRA_THEME_DIR . 'inc/metabox/class-astra-elementor-editor-settings.php';

require_once ASTRA_THEME_DIR . 'inc/customizer/class-astra-customizer.php';

require_once ASTRA_THEME_DIR . 'inc/modules/posts-structures/class-astra-post-structures.php';
require_once ASTRA_THEME_DIR . 'inc/modules/related-posts/class-astra-related-posts.php';

require_once ASTRA_THEME_DIR . 'inc/compatibility/class-astra-gutenberg.php';
require_once ASTRA_THEME_DIR . 'inc/compatibility/class-astra-jetpack.php';
require_once ASTRA_THEME_DIR . 'inc/compatibility/woocommerce/class-astra-woocommerce.php';
require_once ASTRA_THEME_DIR . 'inc/compatibility/edd/class-astra-edd.php';
require_once ASTRA_THEME_DIR . 'inc/compatibility/lifterlms/class-astra-lifterlms.php';
require_once ASTRA_THEME_DIR . 'inc/compatibility/learndash/class-astra-learndash.php';
require_once ASTRA_THEME_DIR . 'inc/compatibility/class-astra-beaver-builder.php';
require_once ASTRA_THEME_DIR . 'inc/compatibility/class-astra-bb-ultimate-addon.php';
require_once ASTRA_THEME_DIR . 'inc/compatibility/class-astra-contact-form-7.php';
require_once ASTRA_THEME_DIR . 'inc/compatibility/class-astra-visual-composer.php';
require_once ASTRA_THEME_DIR . 'inc/compatibility/class-astra-site-origin.php';
require_once ASTRA_THEME_DIR . 'inc/compatibility/class-astra-gravity-forms.php';
require_once ASTRA_THEME_DIR . 'inc/compatibility/class-astra-bne-flyout.php';
require_once ASTRA_THEME_DIR . 'inc/compatibility/class-astra-ubermeu.php';
require_once ASTRA_THEME_DIR . 'inc/compatibility/class-astra-divi-builder.php';
require_once ASTRA_THEME_DIR . 'inc/compatibility/class-astra-amp.php';
require_once ASTRA_THEME_DIR . 'inc/compatibility/class-astra-yoast-seo.php';
require_once ASTRA_THEME_DIR . 'inc/compatibility/surecart/class-astra-surecart.php';
require_once ASTRA_THEME_DIR . 'inc/compatibility/class-astra-starter-content.php';
require_once ASTRA_THEME_DIR . 'inc/compatibility/class-astra-buddypress.php';
require_once ASTRA_THEME_DIR . 'inc/addons/transparent-header/class-astra-ext-transparent-header.php';
require_once ASTRA_THEME_DIR . 'inc/addons/breadcrumbs/class-astra-breadcrumbs.php';
require_once ASTRA_THEME_DIR . 'inc/addons/scroll-to-top/class-astra-scroll-to-top.php';
require_once ASTRA_THEME_DIR . 'inc/addons/heading-colors/class-astra-heading-colors.php';
require_once ASTRA_THEME_DIR . 'inc/builder/class-astra-builder-loader.php';

if ( version_compare( PHP_VERSION, '5.4', '>=' ) ) {
	require_once ASTRA_THEME_DIR . 'inc/compatibility/class-astra-elementor.php';
	require_once ASTRA_THEME_DIR . 'inc/compatibility/class-astra-elementor-pro.php';
	require_once ASTRA_THEME_DIR . 'inc/compatibility/class-astra-web-stories.php';
}

if ( version_compare( PHP_VERSION, '5.3', '>=' ) ) {
	require_once ASTRA_THEME_DIR . 'inc/compatibility/class-astra-beaver-themer.php';
}

require_once ASTRA_THEME_DIR . 'inc/core/markup/class-astra-markup.php';

require_once ASTRA_THEME_DIR . 'inc/abilities/bootstrap.php';

require_once ASTRA_THEME_DIR . 'inc/core/deprecated/deprecated-filters.php';
require_once ASTRA_THEME_DIR . 'inc/core/deprecated/deprecated-hooks.php';
require_once ASTRA_THEME_DIR . 'inc/core/deprecated/deprecated-functions.php';

/* ==========================================================
   지역 커스텀 택소노미
   ========================================================== */
function noinjob_register_region_taxonomy() {
    register_taxonomy( 'job_region', [ 'post' ], [
        'labels' => [
            'name'          => '지역',
            'singular_name' => '지역',
            'menu_name'     => '지역별',
            'all_items'     => '전체 지역',
            'add_new_item'  => '새 지역 추가',
        ],
        'hierarchical'       => false,
        'public'             => true,
        'show_ui'            => true,
        'show_in_rest'       => true,
        'rest_base'          => 'job_region',
        'show_in_nav_menus'  => true,
        'show_admin_column'  => true,
        'rewrite'            => [ 'slug' => 'region' ],
        'query_var'          => true,
    ] );
}
add_action( 'init', 'noinjob_register_region_taxonomy' );

/* ==========================================================
   노인잡 홈페이지 쇼트코드
   ========================================================== */
function noinjob_home_shortcode() {
    $senuri_posts = get_posts(['numberposts' => 6, 'cat' => 2, 'post_status' => 'publish']);
    $welfare_posts = get_posts(['numberposts' => 3, 'cat' => 3, 'post_status' => 'publish']);
    $column_posts  = get_posts(['numberposts' => 3, 'category_name' => '칼럼', 'post_status' => 'publish']);

    $today      = date('Y-m-d');
    $week_later = date('Y-m-d', strtotime('+7 days'));
    $deadline_posts = get_posts([
        'numberposts' => 6,
        'cat'         => 2,
        'post_status' => 'publish',
        'meta_query'  => [[
            'key'     => '_deadline',
            'value'   => [$today, $week_later],
            'compare' => 'BETWEEN',
            'type'    => 'DATE',
        ]],
        'meta_key' => '_deadline',
        'orderby'  => 'meta_value',
        'order'    => 'ASC',
    ]);

    ob_start(); ?>

    <!-- ===== 히어로 ===== -->
    <div class="nih-hero">
        <div class="nih-hero-inner">
            <h1 class="nih-hero-title">전국 어르신 일자리 · 복지 통합 정보</h1>
            <p class="nih-hero-sub">매일 업데이트되는 시니어 채용 공고와 복지 서비스를 한곳에서 확인하세요</p>

            <div class="nih-search-wrap">
                <form role="search" method="get" action="<?php echo esc_url( home_url('/') ); ?>">
                    <div class="nih-search-box">
                        <input type="search" class="nih-search-input"
                               placeholder="노인일자리, 복지혜택 검색..."
                               name="s"
                               value="<?php echo esc_attr( get_search_query() ); ?>">
                        <button type="submit" class="nih-search-btn">검색</button>
                    </div>
                </form>
            </div>

            <div class="nih-stats">
                <div class="nih-stat"><span class="nih-stat-num">500+</span><span class="nih-stat-label">노인일자리 공고</span></div>
                <div class="nih-stat"><span class="nih-stat-num">390+</span><span class="nih-stat-label">복지 서비스</span></div>
                <div class="nih-stat"><span class="nih-stat-num">30+</span><span class="nih-stat-label">전문 칼럼</span></div>
                <div class="nih-stat"><span class="nih-stat-num">매일</span><span class="nih-stat-label">업데이트</span></div>
            </div>
        </div>
    </div>

    <!-- ===== 카테고리 스트립 ===== -->
    <div class="nih-cats-wrap">
        <div class="nih-cats-grid">
            <a href="/category/senior-job" class="nih-cat-card">
                <div class="nih-cat-icon">💼</div>
                <div class="nih-cat-info">
                    <h3>노인일자리</h3>
                    <p>전국 시니어 채용 공고 모음</p>
                </div>
            </a>
            <a href="/category/welfare" class="nih-cat-card">
                <div class="nih-cat-icon">🏥</div>
                <div class="nih-cat-info">
                    <h3>복지혜택</h3>
                    <p>정부 복지 서비스 안내</p>
                </div>
            </a>
            <a href="/category/column" class="nih-cat-card">
                <div class="nih-cat-icon">📋</div>
                <div class="nih-cat-info">
                    <h3>전문 칼럼</h3>
                    <p>시니어 생활 전문 정보</p>
                </div>
            </a>
        </div>
    </div>

    <!-- ===== 본문 컨텐츠 ===== -->
    <div class="nih-body-wrap">
        <div class="nih-inner">

            <?php if ( $deadline_posts ) : ?>
            <div class="nih-section">
                <div class="nih-section-head">
                    <h2>🔥 마감임박 공고</h2>
                    <a href="/category/senior-job" class="nih-more-link">전체보기 →</a>
                </div>
                <div class="nih-posts-grid">
                    <?php foreach ( $deadline_posts as $post ) :
                        $deadline  = get_post_meta( $post->ID, '_deadline', true );
                        $diff      = (int) ceil( ( strtotime($deadline) - strtotime($today) ) / 86400 );
                        $dday      = $diff === 0 ? 'D-DAY' : 'D-' . $diff;
                        $dday_cls  = $diff <= 2 ? 'nih-dday-red' : 'nih-dday-orange';
                    ?>
                    <a href="<?php echo esc_url( get_permalink($post) ); ?>" class="nih-post-card">
                        <div class="nih-post-meta">
                            <span class="nih-post-badge">노인일자리</span>
                            <span class="nih-dday-badge <?php echo $dday_cls; ?>"><?php echo esc_html($dday); ?></span>
                        </div>
                        <div class="nih-post-title"><?php echo esc_html( get_the_title($post) ); ?></div>
                        <div class="nih-post-excerpt"><?php echo esc_html( wp_trim_words( get_the_excerpt($post), 15 ) ); ?></div>
                        <div class="nih-post-footer">마감 <?php echo esc_html($deadline); ?></div>
                    </a>
                    <?php endforeach; ?>
                </div>
            </div>
            <?php endif; ?>

            <?php if ( $senuri_posts ) : ?>
            <div class="nih-section">
                <div class="nih-section-head">
                    <h2>최신 노인일자리 공고</h2>
                    <a href="/category/senior-job" class="nih-more-link">전체보기 →</a>
                </div>
                <div class="nih-posts-grid">
                    <?php foreach ( $senuri_posts as $post ) : ?>
                    <a href="<?php echo esc_url( get_permalink($post) ); ?>" class="nih-post-card">
                        <div class="nih-post-meta">
                            <span class="nih-post-badge">노인일자리</span>
                            <span class="nih-post-date"><?php echo get_the_date('Y.m.d', $post); ?></span>
                        </div>
                        <div class="nih-post-title"><?php echo esc_html( get_the_title($post) ); ?></div>
                        <div class="nih-post-excerpt"><?php echo esc_html( wp_trim_words( get_the_excerpt($post), 15 ) ); ?></div>
                        <div class="nih-post-footer"><?php echo get_the_date('Y.m.d', $post); ?></div>
                    </a>
                    <?php endforeach; ?>
                </div>
            </div>
            <?php endif; ?>

            <?php if ( $column_posts ) : ?>
            <div class="nih-section">
                <div class="nih-section-head">
                    <h2>전문 칼럼</h2>
                    <a href="/category/column" class="nih-more-link">전체보기 →</a>
                </div>
                <div class="nih-posts-grid">
                    <?php foreach ( $column_posts as $post ) : ?>
                    <a href="<?php echo esc_url( get_permalink($post) ); ?>" class="nih-post-card">
                        <div class="nih-post-meta">
                            <span class="nih-post-badge nih-badge-column">칼럼</span>
                            <span class="nih-post-date"><?php echo get_the_date('Y.m.d', $post); ?></span>
                        </div>
                        <div class="nih-post-title"><?php echo esc_html( get_the_title($post) ); ?></div>
                        <div class="nih-post-excerpt"><?php echo esc_html( wp_trim_words( get_the_excerpt($post), 20 ) ); ?></div>
                        <div class="nih-post-footer"><?php echo get_the_date('Y.m.d', $post); ?></div>
                    </a>
                    <?php endforeach; ?>
                </div>
            </div>
            <?php endif; ?>

            <?php if ( $welfare_posts ) : ?>
            <div class="nih-section">
                <div class="nih-section-head">
                    <h2>복지혜택 정보</h2>
                    <a href="/category/welfare" class="nih-more-link">전체보기 →</a>
                </div>
                <div class="nih-posts-grid">
                    <?php foreach ( $welfare_posts as $post ) : ?>
                    <a href="<?php echo esc_url( get_permalink($post) ); ?>" class="nih-post-card">
                        <div class="nih-post-meta">
                            <span class="nih-post-badge nih-badge-welfare">복지혜택</span>
                            <span class="nih-post-date"><?php echo get_the_date('Y.m.d', $post); ?></span>
                        </div>
                        <div class="nih-post-title"><?php echo esc_html( get_the_title($post) ); ?></div>
                        <div class="nih-post-excerpt"><?php echo esc_html( wp_trim_words( get_the_excerpt($post), 20 ) ); ?></div>
                        <div class="nih-post-footer"><?php echo get_the_date('Y.m.d', $post); ?></div>
                    </a>
                    <?php endforeach; ?>
                </div>
            </div>
            <?php endif; ?>

        </div><!-- .nih-inner -->
    </div><!-- .nih-body-wrap -->

<?php
    return ob_get_clean();
}
add_shortcode( 'noinjob_home', 'noinjob_home_shortcode' );


/* ==========================================================
   _deadline 메타 필드 REST API 등록
   ========================================================== */
add_action( 'init', function() {
    register_post_meta( 'post', '_deadline', [
        'show_in_rest'  => true,
        'single'        => true,
        'type'          => 'string',
        'auth_callback' => function() {
            return current_user_can( 'edit_posts' );
        },
    ]);
});


/* ==========================================================
   보안: WordPress 버전 노출 제거
   ========================================================== */
remove_action( 'wp_head', 'wp_generator' );
remove_action( 'wp_head', 'wlwmanifest_link' );
remove_action( 'wp_head', 'rsd_link' );


/* ==========================================================
   구조화 데이터 (Schema.org)
   ========================================================== */
function noinjob_schema_markup() {

    // 홈페이지: WebSite + SearchAction
    if ( is_front_page() ) {
        $schema = [
            '@context'        => 'https://schema.org',
            '@type'           => 'WebSite',
            'name'            => '노인일자리 - 어르신 구인정보 통합 검색',
            'url'             => home_url(),
            'description'     => '전국 어르신 일자리 공고와 복지혜택 정보를 한곳에서 확인하세요.',
            'potentialAction' => [
                '@type'       => 'SearchAction',
                'target'      => [
                    '@type'       => 'EntryPoint',
                    'urlTemplate' => home_url( '/?s={search_term_string}' ),
                ],
                'query-input' => 'required name=search_term_string',
            ],
            'publisher' => [
                '@type' => 'Organization',
                'name'  => '노인일자리',
                'url'   => home_url(),
            ],
        ];
        echo '<script type="application/ld+json">'
            . json_encode( $schema, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES | JSON_PRETTY_PRINT )
            . '</script>' . "\n";
    }

    // 단일 포스트
    if ( is_singular( 'post' ) ) {
        $post_id     = get_the_ID();
        $cats        = wp_get_post_categories( $post_id, [ 'fields' => 'slugs' ] );
        $title       = get_the_title( $post_id );
        $excerpt     = wp_strip_all_tags( get_the_excerpt( $post_id ) );
        $date_posted = get_the_date( 'c', $post_id );
        $deadline    = get_post_meta( $post_id, '_deadline', true );

        if ( in_array( 'senior-job', $cats, true ) ) {
            // 노인일자리 → JobPosting (구글 채용공고 리치 결과)
            $schema = [
                '@context'          => 'https://schema.org',
                '@type'             => 'JobPosting',
                'title'             => $title,
                'description'       => $excerpt ?: $title,
                'datePosted'        => $date_posted,
                'url'               => get_permalink( $post_id ),
                'employmentType'    => 'PART_TIME',
                'hiringOrganization' => [
                    '@type'  => 'Organization',
                    'name'   => '노인일자리',
                    'sameAs' => home_url(),
                ],
                'jobLocation' => [
                    '@type'   => 'Place',
                    'address' => [
                        '@type'          => 'PostalAddress',
                        'addressCountry' => 'KR',
                    ],
                ],
            ];
            if ( $deadline ) {
                $schema['validThrough'] = $deadline . 'T23:59:59';
            }
        } else {
            // 복지혜택·칼럼 → Article
            $schema = [
                '@context'      => 'https://schema.org',
                '@type'         => 'Article',
                'headline'      => $title,
                'description'   => $excerpt ?: $title,
                'url'           => get_permalink( $post_id ),
                'datePublished' => $date_posted,
                'dateModified'  => get_the_modified_date( 'c', $post_id ),
                'author'        => [ '@type' => 'Organization', 'name' => '노인일자리' ],
                'publisher'     => [ '@type' => 'Organization', 'name' => '노인일자리', 'url' => home_url() ],
            ];
        }
        echo '<script type="application/ld+json">'
            . json_encode( $schema, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES | JSON_PRETTY_PRINT )
            . '</script>' . "\n";
    }

    // 카테고리 아카이브: BreadcrumbList
    if ( is_category() ) {
        $cat    = get_queried_object();
        $schema = [
            '@context'        => 'https://schema.org',
            '@type'           => 'BreadcrumbList',
            'itemListElement' => [
                [ '@type' => 'ListItem', 'position' => 1, 'name' => '홈',      'item' => home_url() ],
                [ '@type' => 'ListItem', 'position' => 2, 'name' => $cat->name, 'item' => get_category_link( $cat->term_id ) ],
            ],
        ];
        echo '<script type="application/ld+json">'
            . json_encode( $schema, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES | JSON_PRETTY_PRINT )
            . '</script>' . "\n";
    }
}
add_action( 'wp_head', 'noinjob_schema_markup' );

