# business_modules.contacts.campaigns

## Imports
- core_modules.organization.models
- django.conf
- django.core.exceptions
- django.db
- django.utils.translation
- leads

## Classes
- CampaignType
  - attr: `EMAIL`
  - attr: `WEBINAR`
  - attr: `CONFERENCE`
  - attr: `TRADE_SHOW`
  - attr: `ADVERTISEMENT`
  - attr: `DIRECT_MAIL`
  - attr: `OTHER`
- CampaignStatus
  - attr: `PLANNING`
  - attr: `ACTIVE`
  - attr: `COMPLETED`
  - attr: `CANCELLED`
- Campaign
  - attr: `company`
  - attr: `branch`
  - attr: `name`
  - attr: `campaign_type`
  - attr: `status`
  - attr: `start_date`
  - attr: `end_date`
  - attr: `expected_revenue`
  - attr: `budgeted_cost`
  - attr: `actual_cost`
  - attr: `currency`
  - attr: `expected_response_rate`
  - attr: `description`
  - attr: `owner`
  - attr: `created_by`
  - attr: `num_sent`
  - attr: `num_responses`
  - attr: `num_leads_converted`
  - attr: `num_opportunities_created`
  - attr: `created_at`
  - attr: `updated_at`
  - method: `__str__`
- CampaignMemberStatus
  - attr: `PLANNED`
  - attr: `SENT`
  - attr: `RESPONDED`
- CampaignMember
  - attr: `campaign`
  - attr: `lead`
  - attr: `contact`
  - attr: `status`
  - attr: `first_responded_date`
  - attr: `created_at`
  - attr: `updated_at`
  - method: `clean`
  - method: `__str__`
- Meta
  - attr: `verbose_name`
  - attr: `verbose_name_plural`
  - attr: `ordering`
- Meta
  - attr: `verbose_name`
  - attr: `verbose_name_plural`
  - attr: `unique_together`
  - attr: `indexes`

## Functions
- __str__
- clean
- __str__

## Module Variables
- `AUTH_USER_MODEL`
- `__all__`

## Class Diagram

```mermaid
classDiagram
    class CampaignType {
        +EMAIL
        +WEBINAR
        +CONFERENCE
        +TRADE_SHOW
        +ADVERTISEMENT
        +... (2 more)
    }
    class CampaignStatus {
        +PLANNING
        +ACTIVE
        +COMPLETED
        +CANCELLED
    }
    class Campaign {
        +company
        +branch
        +name
        +campaign_type
        +status
        +... (16 more)
        +__str__()
    }
    class CampaignMemberStatus {
        +PLANNED
        +SENT
        +RESPONDED
    }
    class CampaignMember {
        +campaign
        +lead
        +contact
        +status
        +first_responded_date
        +... (2 more)
        +clean()
        +__str__()
    }
    class Meta {
        +verbose_name
        +verbose_name_plural
        +ordering
    }
    class Meta {
        +verbose_name
        +verbose_name_plural
        +unique_together
        +indexes
    }
    CampaignType --> Meta
    CampaignType --> Meta
    CampaignStatus --> Meta
    CampaignStatus --> Meta
    Campaign --> Meta
    Campaign --> Meta
    CampaignMemberStatus --> Meta
    CampaignMemberStatus --> Meta
    CampaignMember --> Meta
    CampaignMember --> Meta
```
