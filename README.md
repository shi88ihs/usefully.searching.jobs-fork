# Useful Job Search Resources for Australia-Based IT Workers

English-only curated job boards and company career pages for an IT worker based in Australia, with a preference for Perth-friendly, remote-friendly, and contract-friendly roles.

## Who this list is for

- Australia-based IT workers, especially people who can work remotely from Perth or similar time zones.
- U.S. citizens living in Australia who can also consider some U.S.-market remote or contractor roles.
- Search focus: IT support, Linux sysadmin, cloud, AWS, DevOps, infrastructure, MSP, field tech, remote support, automation, and security-adjacent IT.

## Eligibility rules

- Keep English-language resources only.
- Prefer Australia, APAC, worldwide, or explicitly remote-friendly roles that can realistically work from Australia.
- Keep U.S. boards only when they support remote international applicants, contractors, or worldwide listings.
- Treat every remote listing as **needs verification** until the posting confirms location, payroll, visa, and tax rules.
- Exclude regional boards that are locked to Brazil, Portugal, Germany, Canada, Chile, New Zealand, and other non-target regions unless a specific role explicitly says otherwise.

## Recommended search keywords

- IT support
- service desk
- help desk
- Linux sysadmin
- systems administrator
- cloud engineer
- AWS
- DevOps
- platform engineer
- infrastructure engineer
- NOC
- SOC
- security operations
- MSP
- field technician
- remote support
- automation engineer
- site reliability engineer
- contractor
- remote Australia
- APAC time zone
- worldwide remote

## 1. Australia IT Job Boards

- [Seek](https://www.seek.com.au) — Australia-focused general board with many IT and support roles.
- [Adzuna Australia](https://www.adzuna.com.au) — Australia board and aggregator; filter carefully by role and location.
- [CareerOne Job View](http://jobview.careerone.com.au) — Australia job board with IT listings.
- [Apply Now AU](http://www.applynow.com.au) — Australia board; verify current role quality and location fit.

## 2. Remote Jobs Open to Australia / APAC / Worldwide

- [Remote Job Worldwide](https://github.com/remoteintech/remote-jobs) — Curated remote-company list with many global options.
- [Remote.co](http://remote.co) — Remote job board and resource hub.
- [Remote OK](http://www.remoteok.io) — Remote-first board with global filters.
- [Remotive](http://remotive.io) — Remote job board focused on distributed roles.
- [We Work Remotely](http://www.weworkremotely.com) — Large remote-first board.
- [Working Nomads](http://www.workingnomads.co/jobs) — Remote board with broad global coverage.
- [Just Remote](https://justremote.co) — Remote-first board with location filters.
- [Wellfound](http://wellfound.com) — Startup board; use remote and location filters carefully.
- [LinkedIn Jobs](https://www.linkedin.com/jobs/) — Use remote and location filters; verify work authorization on each posting.
- [Indeed Worldwide](https://www.indeed.com/worldwide) — Worldwide aggregator; confirm remote eligibility per posting.

## 3. U.S. Citizen-Friendly Remote / Contractor Boards

- [Upwork](https://www.upwork.com) — Freelance marketplace for contract work.
- [Toptal](http://www.toptal.com) — Contract talent network with higher-signal client work.
- [Freelancer](http://www.freelancer.com) — Global freelance marketplace.
- [PeoplePerHour](http://www.peopleperhour.com/freelance-jobs) — Freelance marketplace with contract work.
- [FlexJobs](http://www.flexjobs.com) — Paid remote-job board; verify current listings and geography.
- [Authentic Jobs](http://authenticjobs.com) — Remote-friendly tech jobs and contract roles.

## 4. Cloud, DevOps, Linux, Security, and Infrastructure Roles

Company career pages and role hubs worth watching for infrastructure, platform, and security-adjacent work:

- [1Password](https://www.1password.com) — Security-adjacent company with many remote-friendly roles.
- [Ad Hoc](https://www.adhocteam.us) — Public-sector and infrastructure-focused engineering roles.
- [Airbyte](https://airbyte.com) — Data infrastructure company.
- [Amazon Jobs Virtual Locations](https://www.amazon.jobs/en/locations/virtual-locations) — Needs verification for Australia-based applicants and specific role eligibility.
- [Canonical](https://www.canonical.com) — Linux and open-source infrastructure roles.
- [Cloudflare](https://www.cloudflare.com/careers) — Network, security, and edge infrastructure roles.
- [Datadog](https://www.datadoghq.com) — Observability and infrastructure platform roles.
- [Elastic](https://www.elastic.co) — Search, observability, and security roles.
- [GitLab](https://about.gitlab.com) — Distributed engineering and DevOps culture.
- [HashiCorp](https://www.hashicorp.com) — Infrastructure automation and cloud tooling.
- [Red Hat](https://www.redhat.com) — Linux, open source, and enterprise infrastructure roles.
- [Sentry](https://sentry.io/careers) — Developer tooling and monitoring roles.
- [SUSE](https://www.suse.com) — Linux and enterprise infrastructure roles.
- [Sysdig](https://www.sysdig.org) — Cloud security and observability roles.
- [Tenable](https://www.tenable.com) — Security and vulnerability-management roles.
- [Twilio](https://www.twilio.com) — Cloud communications and platform roles.

## 5. Companies Worth Tracking

- [Automattic](https://automattic.com) — Distributed company with strong remote culture.
- [Basecamp](https://basecamp.com) — Remote-friendly software company.
- [Balsamiq](https://balsamiq.com) — Small distributed company.
- [Bitovi](https://bitovi.com) — Consulting and software engineering roles.
- [Andela](https://andela.com) — Distributed talent network.
- [Shopify](https://www.shopify.com) — Large distributed company; verify region and role.
- [Stripe](https://stripe.com) — Cloud payments company with global roles.
- [X-Team](https://x-team.com) — Remote engineering network.
- [PreviousNext](https://www.previousnext.com.au) — Australia-based digital consultancy.
- [The Iconic](http://www.theiconic.com.au/opportunities) — Australia-based e-commerce employer.

## 6. Freelance and Contract Platforms

For contract, part-time, and freelance work, start with the platforms in section 3.

## 7. Excluded Categories

- Non-English job boards and listings.
- Region-locked boards outside the target geography.
- Dead, redirected, spammy, or low-confidence links.
- Unrelated industries with weak IT value.
- Postings that require local work authorisation or tax residency unless the listing explicitly says otherwise.

## Maintenance notes

- Remote eligibility changes often. Confirm Australia work eligibility before applying.
- Review postings for timezone overlap, contractor status, and payroll location.
- Re-check older links before relying on them for an active application run.

## Link counts

- Links kept: 46
- Links removed or excluded: 1039

## Credits

- Original upstream repository: [atmmoreira/usefully.searching.jobs](https://github.com/atmmoreira/usefully.searching.jobs)
- This fork is an English-only, Australia-focused curation of that original list.

## Link Audit

This repository includes a script to automatically verify and clean up links.

### Requirements
- Python 3
- `requests` (`pip install -r requirements.txt`)

### Running the Audit
Run the script in audit-only mode to generate reports in `reports/`:
```bash
python3 scripts/audit_links.py --input README.md
```

### Applying Fixes
To automatically upgrade HTTP to HTTPS and remove dead links:
```bash
python3 scripts/audit_links.py --input README.md --apply --remove dead,timeout,dns_error,ssl_error
```
This creates a backup at `README.before-link-audit.md` before making any modifications.
