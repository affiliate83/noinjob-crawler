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
   로고 강제 적용 (Customizer 우회)
   - logo.svg가 theme 폴더에 있으므로 Customizer 없이 직접 적용
   ========================================================== */
add_filter( 'get_custom_logo', function( $html ) {
    if ( ! empty( $html ) ) return $html;
    return sprintf(
        '<a href="%s" class="custom-logo-link" rel="home"><img src="%s/logo.svg" class="custom-logo" alt="%s" width="200" height="52" loading="eager"></a>',
        esc_url( home_url( '/' ) ),
        esc_url( get_template_directory_uri() ),
        esc_attr( get_bloginfo( 'name' ) )
    );
}, 20 );

// Astra SVG 아이콘 비활성화 (이미지 로고가 나오도록)
add_filter( 'astra_get_option_site-logo-svg-icon', '__return_false' );


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


/* ==========================================================
   지역 필터 — /category/senior-job 아카이브
   ========================================================== */

// pre_get_posts: ?region=slug 파라미터 → job_region 택소노미 필터
function noinjob_filter_region_query( $query ) {
    if ( is_admin() || ! $query->is_main_query() ) return;
    if ( ! $query->is_category( 'senior-job' ) ) return;
    $region = isset( $_GET['region'] ) ? sanitize_key( $_GET['region'] ) : '';
    if ( $region && $region !== 'all' ) {
        $query->set( 'tax_query', [[
            'taxonomy' => 'job_region',
            'field'    => 'slug',
            'terms'    => $region,
        ]]);
    }
}
add_action( 'pre_get_posts', 'noinjob_filter_region_query' );

// loop_start: 첫 포스트 렌더 직전에 지역 필터 바 HTML 삽입
function noinjob_inject_region_filter( $query ) {
    if ( ! $query->is_main_query() ) return;
    if ( ! $query->is_category( 'senior-job' ) ) return;
    static $done = false;
    if ( $done ) return;
    $done = true;

    $current  = isset( $_GET['region'] ) ? sanitize_key( $_GET['region'] ) : 'all';
    $terms    = get_terms( [
        'taxonomy'   => 'job_region',
        'hide_empty' => true,
        'orderby'    => 'count',
        'order'      => 'DESC',
    ] );
    if ( is_wp_error( $terms ) || empty( $terms ) ) return;

    $base_url = get_category_link( get_queried_object_id() );

    echo '<div class="nih-region-filter">';
    $all_cls = ( $current === 'all' ) ? ' active' : '';
    echo '<a href="' . esc_url( $base_url ) . '" class="nih-region-btn' . $all_cls . '">전체</a>';
    foreach ( $terms as $term ) {
        $cls = ( $current === $term->slug ) ? ' active' : '';
        $url = add_query_arg( 'region', $term->slug, $base_url );
        echo '<a href="' . esc_url( $url ) . '" class="nih-region-btn' . $cls . '">'
            . esc_html( $term->name )
            . '<span class="nih-region-cnt">' . $term->count . '</span>'
            . '</a>';
    }
    echo '</div>';
}
add_action( 'loop_start', 'noinjob_inject_region_filter' );


/* ==========================================================
   단일 포스트 — 지역·모집상태 배지
   ========================================================== */
add_action( 'astra_entry_content_before', function() {
    if ( ! is_singular( 'post' ) ) return;

    $post_id  = get_the_ID();
    $today    = date( 'Y-m-d' );
    $deadline = get_post_meta( $post_id, '_deadline', true );

    // 지역 배지
    $regions     = wp_get_object_terms( $post_id, 'job_region' );
    $region_html = '';
    if ( ! empty( $regions ) && ! is_wp_error( $regions ) ) {
        foreach ( $regions as $r ) {
            $region_html .= '<span class="nih-s-badge nih-s-region">📍 ' . esc_html( $r->name ) . '</span>';
        }
    }

    // 모집 상태 배지
    $status_html = '';
    if ( $deadline ) {
        if ( $deadline < $today ) {
            $status_html = '<span class="nih-s-badge nih-s-closed">마감</span>';
        } elseif ( $deadline === $today ) {
            $status_html = '<span class="nih-s-badge nih-s-open">모집중</span>'
                         . '<span class="nih-s-badge nih-s-dday">D-Day</span>';
        } else {
            $diff        = (int) ceil( ( strtotime( $deadline ) - time() ) / 86400 );
            $status_html = '<span class="nih-s-badge nih-s-open">모집중</span>'
                         . '<span class="nih-s-badge nih-s-dday">D-' . $diff . '</span>';
        }
    }

    if ( ! $region_html && ! $status_html ) return;

    echo '<div class="nih-s-badges">' . $region_html . $status_html . '</div>';
} );

// ──────────────────────────────────────────────────────────
// 노인잡 앱 푸시 토큰 관리 REST API
// ──────────────────────────────────────────────────────────

// 테이블 생성 (최초 1회)
add_action( 'init', function () {
    global $wpdb;
    $table = $wpdb->prefix . 'noinjob_push_tokens';
    if ( $wpdb->get_var( "SHOW TABLES LIKE '$table'" ) !== $table ) {
        $charset = $wpdb->get_charset_collate();
        $wpdb->query( "CREATE TABLE $table (
            id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
            token VARCHAR(300) NOT NULL UNIQUE,
            regions TEXT NOT NULL DEFAULT 'all',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        ) $charset;" );
    }
} );

// REST API 등록
add_action( 'rest_api_init', function () {

    // POST /wp-json/noinjob/v1/push-token — 토큰 등록/업데이트
    register_rest_route( 'noinjob/v1', '/push-token', [
        'methods'             => 'POST',
        'callback'            => function ( $req ) {
            global $wpdb;
            $token   = sanitize_text_field( $req->get_param('token') );
            $regions = $req->get_param('regions'); // array

            if ( ! $token ) return new WP_Error( 'no_token', '토큰 없음', [ 'status' => 400 ] );

            $regions_json = is_array( $regions ) ? implode( ',', array_map( 'sanitize_key', $regions ) ) : 'all';

            $table = $wpdb->prefix . 'noinjob_push_tokens';
            $exists = $wpdb->get_var( $wpdb->prepare( "SELECT id FROM $table WHERE token = %s", $token ) );

            if ( $exists ) {
                $wpdb->update( $table, [ 'regions' => $regions_json ], [ 'token' => $token ] );
            } else {
                $wpdb->insert( $table, [ 'token' => $token, 'regions' => $regions_json ] );
            }
            return [ 'success' => true ];
        },
        'permission_callback' => '__return_true',
    ] );

    // GET /wp-json/noinjob/v1/push-tokens?region=seoul — 지역별 토큰 조회 (크롤러용)
    register_rest_route( 'noinjob/v1', '/push-tokens', [
        'methods'             => 'GET',
        'callback'            => function ( $req ) {
            global $wpdb;
            $region = sanitize_key( $req->get_param('region') );
            $table  = $wpdb->prefix . 'noinjob_push_tokens';

            if ( $region ) {
                $rows = $wpdb->get_col( $wpdb->prepare(
                    "SELECT token FROM $table WHERE regions = 'all' OR FIND_IN_SET(%s, regions) > 0",
                    $region
                ) );
            } else {
                $rows = $wpdb->get_col( "SELECT token FROM $table" );
            }
            return [ 'tokens' => $rows ];
        },
        'permission_callback' => '__return_true',
    ] );

    // GET /wp-json/noinjob/v1/send-push-now?secret=XXX&type=job|column|welfare
    register_rest_route( 'noinjob/v1', '/send-push-now', [
        'methods'             => 'GET',
        'callback'            => function ( $req ) {
            // 인증
            $secret   = sanitize_text_field( $req->get_param('secret') );
            $expected = get_option( 'noinjob_push_secret', '' );
            if ( ! $expected || ! hash_equals( $expected, $secret ) ) {
                return new WP_Error( 'forbidden', '인증 실패', [ 'status' => 403 ] );
            }

            $type  = sanitize_key( $req->get_param('type') ?: 'job' );
            $today = date( 'Y-m-d' );

            global $wpdb;
            $table = $wpdb->prefix . 'noinjob_push_tokens';
            $rows  = $wpdb->get_results( "SELECT token, regions FROM $table" );
            if ( empty( $rows ) ) {
                return [ 'success' => true, 'sent' => 0, 'message' => '등록된 토큰 없음' ];
            }

            $messages = [];

            // ── 12:00 칼럼 알림 ──────────────────────────────
            if ( $type === 'column' ) {
                $col = get_posts( [
                    'numberposts' => 1,
                    'category_name' => 'column',
                    'post_status' => 'publish',
                    'orderby' => 'date', 'order' => 'DESC',
                ] );
                if ( empty( $col ) ) return [ 'success' => true, 'sent' => 0, 'message' => '칼럼 없음' ];
                $col_title = get_the_title( $col[0]->ID );
                foreach ( $rows as $row ) {
                    $messages[] = [
                        'to'    => $row->token,
                        'title' => '📋 새 칼럼이 올라왔습니다',
                        'body'  => $col_title,
                        'data'  => [ 'screen' => 'Column' ],
                        'sound' => 'default',
                    ];
                }

            // ── 19:00 복지혜택 알림 ──────────────────────────
            } elseif ( $type === 'welfare' ) {
                $welfare = get_posts( [
                    'numberposts' => 1,
                    'cat'         => 3,
                    'post_status' => 'publish',
                    'orderby' => 'date', 'order' => 'DESC',
                ] );
                if ( empty( $welfare ) ) return [ 'success' => true, 'sent' => 0, 'message' => '복지혜택 없음' ];
                $w_title = get_the_title( $welfare[0]->ID );
                foreach ( $rows as $row ) {
                    $messages[] = [
                        'to'    => $row->token,
                        'title' => '🏥 복지혜택 정보',
                        'body'  => $w_title,
                        'data'  => [ 'screen' => 'Welfare' ],
                        'sound' => 'default',
                    ];
                }

            // ── 09:00 일자리 알림 ────────────────────────────
            } else {
                // 오늘 새 일자리 공고
                $job_posts = get_posts( [
                    'numberposts' => -1,
                    'cat'         => 2,
                    'post_status' => 'publish',
                    'date_query'  => [ [ 'after' => $today . ' 00:00:00', 'inclusive' => true ] ],
                    'orderby' => 'date', 'order' => 'DESC',
                ] );
                if ( empty( $job_posts ) ) return [ 'success' => true, 'sent' => 0, 'message' => '새 일자리 공고 없음' ];

                // 지역별 집계
                $region_map = [];
                foreach ( $job_posts as $post ) {
                    $terms = wp_get_object_terms( $post->ID, 'job_region' );
                    if ( ! is_wp_error( $terms ) ) {
                        foreach ( $terms as $term ) {
                            if ( ! isset( $region_map[ $term->slug ] ) )
                                $region_map[ $term->slug ] = [ 'name' => $term->name, 'count' => 0 ];
                            $region_map[ $term->slug ]['count']++;
                        }
                    }
                }

                // 최신 칼럼 1건 (지역 설정 사용자용 추가 정보)
                $col = get_posts( [
                    'numberposts' => 1,
                    'category_name' => 'column',
                    'post_status' => 'publish',
                    'orderby' => 'date', 'order' => 'DESC',
                ] );
                $col_suffix = ! empty( $col ) ? ' · 칼럼 1건' : '';

                $total     = count( $job_posts );
                $gen_title = '📢 새 노인일자리 공고';
                $gen_body  = $total > 1
                    ? get_the_title( $job_posts[0]->ID ) . ' 외 ' . ( $total - 1 ) . '건'
                    : get_the_title( $job_posts[0]->ID );

                foreach ( $rows as $row ) {
                    $user_regions = array_map( 'trim', explode( ',', $row->regions ) );
                    $has_region   = ! in_array( 'all', $user_regions, true ) && ! empty( array_filter( $user_regions ) );

                    if ( $has_region ) {
                        // 지역 설정 사용자 → 해당 지역 새 공고 + 칼럼
                        foreach ( $user_regions as $slug ) {
                            if ( isset( $region_map[ $slug ] ) ) {
                                $info       = $region_map[ $slug ];
                                $messages[] = [
                                    'to'    => $row->token,
                                    'title' => '📍 ' . $info['name'] . ' 새 소식',
                                    'body'  => '새 일자리 ' . $info['count'] . '건' . $col_suffix,
                                    'data'  => [ 'screen' => 'Jobs' ],
                                    'sound' => 'default',
                                ];
                                break;
                            }
                        }
                    } else {
                        // 일반 사용자 → 전체 일자리 공고
                        $messages[] = [
                            'to'    => $row->token,
                            'title' => $gen_title,
                            'body'  => $gen_body,
                            'data'  => [ 'screen' => 'Jobs' ],
                            'sound' => 'default',
                        ];
                    }
                }
            }

            if ( empty( $messages ) ) {
                return [ 'success' => true, 'sent' => 0, 'message' => '발송 대상 없음' ];
            }

            // Expo Push API 발송
            $sent = 0; $errors = 0;
            foreach ( array_chunk( $messages, 100 ) as $chunk ) {
                $res = wp_remote_post( 'https://exp.host/--/api/v2/push/send', [
                    'headers' => [ 'Content-Type' => 'application/json', 'Accept' => 'application/json' ],
                    'body'    => wp_json_encode( $chunk ),
                    'timeout' => 30,
                ] );
                if ( is_wp_error( $res ) ) { $errors++; } else { $sent += count( $chunk ); }
            }

            return [ 'success' => true, 'type' => $type, 'sent' => $sent, 'errors' => $errors ];
        },
        'permission_callback' => '__return_true',
    ] );

} ); // end rest_api_init

// app-ads.txt — AdMob 앱 인증용
add_action( 'init', function () {
    $uri = parse_url( $_SERVER['REQUEST_URI'] ?? '', PHP_URL_PATH );
    if ( $uri === '/app-ads.txt' ) {
        header( 'Content-Type: text/plain; charset=utf-8' );
        echo "google.com, pub-9578724205171459, DIRECT, f08c47fec0942fa0\n";
        exit;
    }
} );

// robots.txt에 sitemap 경로 추가 (애드센스 크롤러·Googlebot용)
add_filter( 'robots_txt', function ( $output ) {
    if ( strpos( $output, 'sitemap_index.xml' ) === false ) {
        $output .= "\nSitemap: https://noinjob.kr/sitemap_index.xml\n";
    }
    return $output;
}, 10, 1 );

