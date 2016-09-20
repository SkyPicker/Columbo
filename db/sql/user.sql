-- name: select-user-by-id
-- Select user by id
SELECT * FROM user WHERE id=:id;

-- name: select-all-users
-- Select all github users
SELECT login FROM user;

-- name: select-public-repos
-- Select all public repositories
SELECT id, repos_url FROM user WHERE public_repos > 0;

-- name: update-user
-- Update github user
UPDATE "user"
SET login=:login,
    avatar_url=:avatar_url,
    gravatar_id=:gravatar_id,
    url=:url,
    html_url=:html_url,
    followers_url=:followers_url,
    following_url=:following_url,
    gists_url=:gists_url,
    starred_url=:starred_url,
    subscriptions_url=:subscriptions_url,
    organizations_url=:organizations_url,
    repos_url=:repos_url,
    events_url=:events_url,
    received_events_url=:received_events_url,
    type=:type,
    site_admin=:site_admin,
    name=:name,
    company=:company,
    blog=:blog,
    location=:location,
    email=:email,
    hireable=:hireable,
    bio=:bio,
    public_repos=:public_repos,
    public_gists=:public_gists,
    followers=:followers,
    following=:following,
    created_at=:created_at,
    updated_at=:updated_at
WHERE
    id=:id;

-- name: insert-user
-- Insert github user
INSERT INTO "user" (
        id,
        login,
        avatar_url,
        gravatar_id,
        url,
        html_url,
        followers_url,
        following_url,
        gists_url,
        starred_url,
        subscriptions_url,
        organizations_url,
        repos_url,
        events_url,
        received_events_url,
        type,
        site_admin,
        name,
        company,
        blog,
        location,
        email,
        hireable,
        bio,
        public_repos,
        public_gists,
        followers,
        following,
        created_at,
        updated_at
) VALUES (
    :id,
    :login,
    :avatar_url,
    :gravatar_id,
    :url,
    :html_url,
    :followers_url,
    :following_url,
    :gists_url,
    :starred_url,
    :subscriptions_url,
    :organizations_url,
    :repos_url,
    :events_url,
    :received_events_url,
    :type,
    :site_admin,
    :name,
    :company,
    :blog,
    :location,
    :email,
    :hireable,
    :bio,
    :public_repos,
    :public_gists,
    :followers,
    :following,
    :created_at,
    :updated_at
);
